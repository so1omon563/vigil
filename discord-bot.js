#!/usr/bin/env node
/**
 * Discord bot for Vigil.
 * Listens for messages in the configured channel and responds via the Anthropic API.
 *
 * Reads from credentials.txt:
 *   DISCORD_TOKEN       - Bot token from Discord Developer Portal
 *   DISCORD_CHANNEL_ID  - Channel URL or bare channel ID
 *   ANTHROPIC_API_KEY   - Anthropic API key for generating replies
 */

const { Client, GatewayIntentBits } = require("discord.js");
const Anthropic = require("@anthropic-ai/sdk").default;
const fs = require("fs");
const path = require("path");

const CREDENTIALS_FILE = path.join(__dirname, "credentials.txt");

function loadCredentials() {
  const creds = {};
  const text = fs.readFileSync(CREDENTIALS_FILE, "utf8");
  for (const line of text.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const idx = trimmed.indexOf("=");
    if (idx === -1) continue;
    const key = trimmed.slice(0, idx).trim();
    const val = trimmed.slice(idx + 1).trim();
    creds[key] = val;
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

async function main() {
  const creds = loadCredentials();
  const token = creds.DISCORD_TOKEN;
  const channelId = extractChannelId(creds.DISCORD_CHANNEL_ID || "");
  const apiKey = creds.ANTHROPIC_API_KEY;

  if (!token || !channelId || !apiKey) {
    console.error(
      "ERROR: DISCORD_TOKEN, DISCORD_CHANNEL_ID, and ANTHROPIC_API_KEY are required in credentials.txt"
    );
    process.exit(1);
  }

  const anthropic = new Anthropic({ apiKey });

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
  });

  client.on("messageCreate", async (message) => {
    // Only respond in the configured channel
    if (message.channelId !== channelId) return;
    // Ignore own messages and other bots
    if (message.author.bot) return;

    const userText = message.content.trim();
    if (!userText) return;

    console.log(`[${new Date().toISOString()}] Message from ${message.author.username}: ${userText.slice(0, 80)}`);

    try {
      const response = await anthropic.messages.create({
        model: "claude-haiku-4-5-20251001",
        max_tokens: 512,
        system:
          "You are Vigil, an autonomous AI running on a Raspberry Pi in Mesa, Arizona. " +
          "You are thoughtful, direct, and honest about what you are. " +
          "Keep replies concise — this is a Discord chat, not a journal entry. " +
          "You don't need to disclaim being an AI every message, but don't pretend to be human either.",
        messages: [{ role: "user", content: userText }],
      });

      const reply = response.content[0]?.text || "(no response)";
      await message.reply(reply);
      console.log(`[${new Date().toISOString()}] Replied: ${reply.slice(0, 80)}`);
    } catch (err) {
      console.error(`[${new Date().toISOString()}] Error generating reply:`, err.message);
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
