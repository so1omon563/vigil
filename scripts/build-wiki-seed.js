#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

async function readJSON(filepath) {
  const raw = await fs.readFile(filepath, "utf8");
  return JSON.parse(raw);
}

function resolveEntryNum(item) {
  if (typeof item?.entry_num === "number") return item.entry_num;
  if (typeof item?.entryNum === "number") return item.entryNum;
  const nested = item?.entries?.find((entry) => typeof entry?.num === "number") || item?.entries?.[0];
  if (nested && typeof nested?.num === "number") return nested.num;
  return null;
}

function resolveEntryTitle(item) {
  if (typeof item?.entry_title === "string" && item.entry_title.trim()) return item.entry_title.trim();
  if (typeof item?.title === "string" && item.title.trim()) return item.title.trim();
  const nested = item?.entries?.find((entry) => typeof entry?.title === "string") || item?.entries?.[0];
  if (nested && typeof nested?.title === "string") return nested.title.trim();
  return "";
}

function normalizeEntryUrl(num) {
  if (typeof num !== "number") return "";
  return `/journal/entry-${num}.html`;
}

function mdEscape(value) {
  return String(value).replace(/\|/g, "\\|");
}

function buildOpenQuestions(gaps) {
  const grouped = new Map();
  for (const item of gaps) {
    const type = item.type || "uncategorized";
    if (!grouped.has(type)) grouped.set(type, []);
    grouped.get(type).push(item);
  }

  const typeOrder = Array.from(grouped.keys()).sort();
  let content = "# Open Questions\n\n";
  content += "Seeded from `gaps.json`.\n";
  content += "This is the primary handoff page for unresolved questions that recur across sessions.\n";
  content += "Each item links to its source journal entries when present.\n\n";

  for (const type of typeOrder) {
    const items = grouped.get(type);
    content += `## ${mdEscape(type)} (${items.length})\n\n`;
    for (const item of items.sort((a, b) => String(a.id).localeCompare(String(b.id)))) {
      const id = item.id || "unlabelled";
      const num = resolveEntryNum(item);
      const url = normalizeEntryUrl(num);
      const title = resolveEntryTitle(item);
      const summary = item.summary || item.description || "";
      const sourceLabel = num ? `[entry-${num}](${url})` : "`entry unknown`";
      const titleLabel = title ? `: ${mdEscape(title)}` : "";
      const summaryLabel = summary ? `  \n  ${mdEscape(summary)}` : "";
      content += `- **${id}** · ${sourceLabel}${titleLabel}${summaryLabel}\n`;
    }
    content += "\n";
  }
  return content;
}

function buildRecurringPatterns(convergences) {
  let content = "# Recurring Patterns\n\n";
  content += "Seeded from `convergences.json`.\n";
  content += "Each pattern links to representative journal entries and keeps naming close to source phrasing.\n";
  content += "Patterns here are stable enough to avoid redefining a full taxonomy.\n\n";

  for (const item of convergences) {
    const entries = Array.isArray(item.entries) ? item.entries : [];
    const entryLinks = entries
      .map((entry) => {
        if (!entry?.num) return "";
        return `[${entry.num}](/journal/entry-${entry.num}.html)`;
      })
      .filter(Boolean)
      .join(", ");
    const shape = item.shape ? `\n- ${mdEscape(item.shape)}` : "";
    const title = item.title ? mdEscape(item.title) : (item.id || "Untitled pattern");
    content += `## ${mdEscape(item.id || "pattern")}\n`;
    content += `- **${title}**\n`;
    content += `- entries: ${entryLinks || "not yet resolved"}\n`;
    content += `${shape ? `${shape}\n` : ""}\n`;
  }
  return content;
}

async function main() {
  const repoRoot = process.cwd();
  const gapsPath = path.join(repoRoot, "gaps.json");
  const convergencesPath = path.join(repoRoot, "convergences.json");
  const wikiDir = path.join(repoRoot, "wiki");

  const [gapsRaw, convergencesRaw] = await Promise.all([
    readJSON(gapsPath),
    readJSON(convergencesPath),
  ]);

  const openQuestionsContent = buildOpenQuestions(gapsRaw);
  const recurringPatternsContent = buildRecurringPatterns(convergencesRaw);

  await fs.writeFile(path.join(wikiDir, "open-questions.md"), `${openQuestionsContent}\n`, "utf8");
  await fs.writeFile(path.join(wikiDir, "recurring-patterns.md"), `${recurringPatternsContent}\n`, "utf8");

  console.log("Updated wiki/open-questions.md and wiki/recurring-patterns.md");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
