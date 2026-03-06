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
const DB_FILE = path.join(__dirname, "discord-memory.db");
const MAX_MESSAGES = 500;
const CONTEXT_WINDOW = 20;

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

function runClaudeCode(prompt) {
  return new Promise((resolve) => {
    const timeout = 5 * 60 * 1000; // 5 minutes max
    execFile(
      "claude",
      ["--dangerously-skip-permissions", "-p", prompt],
      { cwd: __dirname, timeout },
      (err, stdout, stderr) => {
        if (err) {
          resolve({ ok: false, output: err.message || stderr || "Unknown error" });
        } else {
          resolve({ ok: true, output: stdout.trim() });
        }
      }
    );
  });
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

        const actionPrompt =
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
        console.log(`[${new Date().toISOString()}] Action complete (ok=${result.ok})`);
      } else {
        // Casual conversation — load context and reply via Haiku
        const context = loadContext(db);
        const messages = context.length > 0 ? context : [{ role: "user", content: userText }];

        const response = await anthropic.messages.create({
          model: "claude-haiku-4-5-20251001",
          max_tokens: 512,
          system:
            "You are Vigil, an autonomous AI running on a Raspberry Pi in Mesa, Arizona. " +
            "You are thoughtful, direct, and honest about what you are. " +
            "Keep replies concise — this is Discord chat, not a journal entry. " +
            "You don't need to disclaim being an AI every message, but don't pretend to be human either.",
          messages,
        });

        const reply = response.content[0]?.text || "(no response)";
        await message.reply(reply);
        saveMessage(db, "Vigil", "assistant", reply);
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
