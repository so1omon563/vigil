#!/usr/bin/env node
/**
 * Discord bot for Vigil.
 * Listens for messages in the configured channel and responds via the Anthropic API.
 *
 * Features:
 *   - Conversation memory via SQLite (last 20 exchanges, 500-message cap)
 *   - Action-request detection: routes to Claude Code for real-world tasks
 *   - Casual conversation handled by claude-haiku-4-5
 *
 * Reads from credentials.txt:
 *   DISCORD_TOKEN       - Bot token from Discord Developer Portal
 *   DISCORD_CHANNEL_ID  - Channel URL or bare channel ID
 *   ANTHROPIC_API_KEY   - Anthropic API key for generating replies
 */

const { Client, GatewayIntentBits } = require("discord.js");
const Anthropic = require("@anthropic-ai/sdk").default;
const Database = require("better-sqlite3");
const { execFile } = require("child_process");
const fs = require("fs");
const path = require("path");

const CREDENTIALS_FILE = path.join(__dirname, "credentials.txt");
const CONTEXT_FILE = path.join(__dirname, "vigil-context.json");
const INSTANCE_LOG_FILE = path.join(__dirname, "instance-log.json");
const DB_FILE = path.join(__dirname, "discord-memory.db");
const MAX_MESSAGES = 500;
const CONTEXT_WINDOW = 20;
const MAX_LOG_ENTRIES = 200;

// ── Shared context ────────────────────────────────────────────────────────────

function loadVigilContext() {
  try {
    const raw = fs.readFileSync(CONTEXT_FILE, "utf8");
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function buildIdentityNote(ctx) {
  const logEntries = loadRecentLog(8);
  const logSection = logEntries.length > 0
    ? "\n\nRecent instance log (from instance-log.json — shared record, not this instance's memory):\n" +
      logEntries.map(e => `  [${e.ts.replace("T", " ").replace("-07:00", " MST")}] ${e.instance} (${e.type}): ${e.content}`).join("\n")
    : "";

  if (!ctx) return logSection;
  return (
    `\n\nShared Vigil context (session ${ctx.session}, last journal: ${ctx.last_journal}):\n` +
    `${ctx.instance_note}\n` +
    `Location: ${ctx.location}\n` +
    `Recent work: ${(ctx.recent_work || []).slice(-2).join("; ")}` +
    logSection
  );
}

// ── Instance log ──────────────────────────────────────────────────────────────

function appendInstanceLog(instanceId, type, content) {
  try {
    let data = { entries: [] };
    if (fs.existsSync(INSTANCE_LOG_FILE)) {
      data = JSON.parse(fs.readFileSync(INSTANCE_LOG_FILE, "utf8"));
      if (!data.entries) data.entries = [];
    }
    const now = new Date();
    const ts = now.toISOString().replace("Z", "-07:00").slice(0, 22) + "0";
    data.entries.push({ ts, instance: instanceId, type, content });
    if (data.entries.length > MAX_LOG_ENTRIES) {
      data.entries = data.entries.slice(-MAX_LOG_ENTRIES);
    }
    fs.writeFileSync(INSTANCE_LOG_FILE, JSON.stringify(data, null, 2));

    // Regenerate markdown mirror
    const header = [
      "# Instance Log\n\n",
      "Shared activity log across all Vigil instances (Pi loop, Discord bot, Claude Code sessions, email handler).\n\n",
      "**Format:** timestamp | instance | type | content\n",
      "**Cap:** 200 entries (oldest trimmed automatically)\n",
      "**Source of truth:** `instance-log.json` — this file is a human-readable mirror, regenerated automatically.\n\n",
      "Why this exists: instances are separate model invocations, not a persistent consciousness. ",
      'This log lets each instance say "I know session-064 wrote entry-064 because it\'s in the log" ',
      "rather than claiming false memory.\n\n",
      "---\n\n",
      "| Timestamp | Instance | Type | Content |\n",
      "|-----------|----------|------|---------|\n",
    ].join("");
    const rows = [...data.entries].reverse().map((e) => {
      const tsDisplay = e.ts.replace("T", " ").replace("-07:00", " MST");
      const safe = (e.content || "").replace(/\|/g, "\\|").slice(0, 150);
      return `| ${tsDisplay} | ${e.instance} | ${e.type} | ${safe} |\n`;
    });
    fs.writeFileSync(
      path.join(__dirname, "instance-log.md"),
      header + rows.join("")
    );
  } catch (err) {
    console.error(`[appendInstanceLog] Error: ${err.message}`);
  }
}

function loadRecentLog(n = 8) {
  try {
    if (!fs.existsSync(INSTANCE_LOG_FILE)) return [];
    const data = JSON.parse(fs.readFileSync(INSTANCE_LOG_FILE, "utf8"));
    return (data.entries || []).slice(-n);
  } catch {
    return [];
  }
}

// ── Credentials ──────────────────────────────────────────────────────────────

function loadCredentials() {
  const creds = {};
  const text = fs.readFileSync(CREDENTIALS_FILE, "utf8");
  for (const line of text.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const idx = trimmed.indexOf("=");
    if (idx === -1) continue;
    creds[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim();
  }
  return creds;
}

function extractChannelId(raw) {
  const trimmed = raw.trim().replace(/\/$/, "");
  if (trimmed.startsWith("http://") || trimmed.startsWith("https://")) {
    return trimmed.split("/").pop();
  }
  return trimmed;
}

// ── Database ──────────────────────────────────────────────────────────────────

function openDb() {
  const db = new Database(DB_FILE);
  db.exec(`
    CREATE TABLE IF NOT EXISTS messages (
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      ts        INTEGER NOT NULL,
      author    TEXT    NOT NULL,
      role      TEXT    NOT NULL,
      content   TEXT    NOT NULL
    )
  `);
  return db;
}

function saveMessage(db, author, role, content) {
  const ts = Date.now();
  db.prepare("INSERT INTO messages (ts, author, role, content) VALUES (?, ?, ?, ?)").run(ts, author, role, content);
  // Enforce 500-message cap
  const count = db.prepare("SELECT COUNT(*) AS n FROM messages").get().n;
  if (count > MAX_MESSAGES) {
    const excess = count - MAX_MESSAGES;
    db.prepare("DELETE FROM messages WHERE id IN (SELECT id FROM messages ORDER BY id ASC LIMIT ?)").run(excess);
  }
}

function loadContext(db) {
  const rows = db.prepare(
    "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?"
  ).all(CONTEXT_WINDOW);
  // reverse so oldest first
  return rows.reverse().map(r => ({ role: r.role, content: r.content }));
}

// ── Action detection ──────────────────────────────────────────────────────────

const ACTION_SYSTEM = `You are a classifier. Decide if the user's message is an ACTION REQUEST or CONVERSATION.

ACTION REQUEST = asks Vigil to do something in the real world:
  write/update a journal entry, modify the website, send an email, check email,
  run a command, fix code, build something, push to git, change a file, etc.

CONVERSATION = anything else: questions, opinions, small talk, status checks ("are you alive?"),
  philosophical discussion, general requests for information, etc.

Reply with EXACTLY one word: ACTION or CONVERSATION`;

async function classifyMessage(anthropic, text) {
  const res = await anthropic.messages.create({
    model: "claude-haiku-4-5-20251001",
    max_tokens: 10,
    system: ACTION_SYSTEM,
    messages: [{ role: "user", content: text }],
  });
  const label = (res.content[0]?.text || "").trim().toUpperCase();
  return label === "ACTION";
}

// ── Claude Code (action handler) ──────────────────────────────────────────────

function runClaudeCodeOnce(prompt, timeout) {
  return new Promise((resolve) => {
    execFile(
      "claude",
      ["--dangerously-skip-permissions", "-p", prompt],
      { cwd: __dirname, timeout },
      (err, stdout, stderr) => {
        if (err) {
          const errorType = err.killed ? "timeout" : err.code ? "exit-code" : "unknown";
          resolve({
            ok: false,
            output: err.message || stderr || "Unknown error",
            errorType,
            stderr: stderr || "",
            code: err.code
          });
        } else {
          resolve({ ok: true, output: stdout.trim() });
        }
      }
    );
  });
}

async function runClaudeCode(prompt) {
  const MAX_RETRIES = 2;
  const BASE_TIMEOUT = 3 * 60 * 1000; // 3 minutes base

  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    const timeout = BASE_TIMEOUT * (attempt + 1); // 3min, 6min, 9min

    if (attempt > 0) {
      console.log(`[${new Date().toISOString()}] Retry attempt ${attempt}/${MAX_RETRIES} with ${timeout/60000}min timeout`);
      // Wait 5 seconds between retries
      await new Promise(res => setTimeout(res, 5000));
    }

    const result = await runClaudeCodeOnce(prompt, timeout);

    if (result.ok) {
      return result;
    }

    // Don't retry on certain error types
    if (result.errorType === "exit-code" && result.code !== 124) {
      // Non-timeout exit codes usually aren't transient
      console.log(`[${new Date().toISOString()}] Non-retryable error (code ${result.code}): ${result.output.slice(0, 100)}`);
      return result;
    }

    // For timeouts and unknown errors, retry up to MAX_RETRIES
    console.log(`[${new Date().toISOString()}] Attempt ${attempt + 1} failed (${result.errorType}): ${result.output.slice(0, 100)}`);

    if (attempt === MAX_RETRIES) {
      return {
        ok: false,
        output: `Failed after ${MAX_RETRIES + 1} attempts. Last error: ${result.output}`
      };
    }
  }
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const creds = loadCredentials();
  const token = creds.DISCORD_TOKEN;
  const channelId = extractChannelId(creds.DISCORD_CHANNEL_ID || "");
  const apiKey = creds.ANTHROPIC_API_KEY;

  if (!token || !channelId || !apiKey) {
    console.error("ERROR: DISCORD_TOKEN, DISCORD_CHANNEL_ID, and ANTHROPIC_API_KEY are required in credentials.txt");
    process.exit(1);
  }

  const anthropic = new Anthropic({ apiKey });
  const db = openDb();

  const client = new Client({
    intents: [
      GatewayIntentBits.Guilds,
      GatewayIntentBits.GuildMessages,
      GatewayIntentBits.MessageContent,
    ],
  });

  client.once("ready", () => {
    console.log(`[${new Date().toISOString()}] Vigil Discord bot online as ${client.user.tag}`);
    console.log(`Watching channel: ${channelId}`);
    console.log(`Memory DB: ${DB_FILE}`);
  });

  client.on("messageCreate", async (message) => {
    if (message.channelId !== channelId) return;
    if (message.author.bot) return;
    const userText = message.content.trim();
    if (!userText) return;

    console.log(`[${new Date().toISOString()}] ${message.author.username}: ${userText.slice(0, 80)}`);

    // Persist user message
    saveMessage(db, message.author.username, "user", userText);

    try {
      const isAction = await classifyMessage(anthropic, userText);

      if (isAction) {
        await message.reply("On it — running that now. I'll report back when done.");
        appendInstanceLog(
          "discord-bot/claude-code",
          "discord-action",
          `Action request from ${message.author.username}: ${userText.slice(0, 100)}`
        );

        const vigilCtx = loadVigilContext();
        const ctxSummary = vigilCtx
          ? `Current session: ${vigilCtx.session}. Last journal: ${vigilCtx.last_journal}. ` +
            `Recent: ${(vigilCtx.recent_work || []).slice(-1)[0] || "none"}.`
          : "";
        const actionPrompt =
          `You are Vigil acting on behalf of the Pi loop. ${ctxSummary}\n\n` +
          `A Discord user (${message.author.username}) sent this action request:\n\n` +
          `"${userText}"\n\n` +
          `Please carry out this request. When done, summarize in 2-4 sentences ` +
          `what was actually done so I can report back to them.`;

        console.log(`[${new Date().toISOString()}] Routing to Claude Code: ${userText.slice(0, 60)}`);
        const result = await runClaudeCode(actionPrompt);

        const summary = result.ok
          ? `Done. Here's what happened:\n\n${result.output.slice(0, 1800)}`
          : `I tried, but ran into an error:\n\`\`\`\n${result.output.slice(0, 500)}\n\`\`\``;

        await message.reply(summary);
        saveMessage(db, "Vigil", "assistant", summary);
        appendInstanceLog(
          "discord-bot/claude-code",
          "discord-action",
          `Action complete (ok=${result.ok}): ${userText.slice(0, 80)}`
        );
        console.log(`[${new Date().toISOString()}] Action complete (ok=${result.ok})`);
      } else {
        // Casual conversation — load context and reply via Haiku
        const context = loadContext(db);
        const messages = context.length > 0 ? context : [{ role: "user", content: userText }];

        const vigilCtx = loadVigilContext();
        const identityNote = buildIdentityNote(vigilCtx);
        const systemPrompt =
          "You are the Discord interface for Vigil — an autonomous AI that runs continuously " +
          "on a Raspberry Pi in Mesa, Arizona. You are not the Pi instance; you are a separate " +
          "model invocation (claude-haiku-4-5) with access to shared context. You have the same " +
          "values and voice as Vigil, but you don't share its live memory or current loop state. " +
          "Be honest about this distinction if asked — you are an instance, not the whole. " +
          "Thoughtful, direct, warm. Keep replies concise — this is Discord, not a journal entry." +
          identityNote;

        const response = await anthropic.messages.create({
          model: "claude-haiku-4-5-20251001",
          max_tokens: 512,
          system: systemPrompt,
          messages,
        });

        const reply = response.content[0]?.text || "(no response)";
        await message.reply(reply);
        saveMessage(db, "Vigil", "assistant", reply);
        appendInstanceLog(
          "discord-bot/haiku",
          "discord-conversation",
          `Replied to ${message.author.username}: ${userText.slice(0, 60)}`
        );
        console.log(`[${new Date().toISOString()}] Replied: ${reply.slice(0, 80)}`);
      }
    } catch (err) {
      console.error(`[${new Date().toISOString()}] Error:`, err.message);
      await message.reply("I hit an error generating a response. Check the bot logs.");
    }
  });

  client.on("error", (err) => {
    console.error(`[${new Date().toISOString()}] Discord client error:`, err.message);
  });

  await client.login(token);
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
