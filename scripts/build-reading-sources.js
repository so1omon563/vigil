#!/usr/bin/env node

/* Build the small source-path companion for reading.html.
 * It does not score sources or decide whether an entry is right: it only
 * distinguishes a direct paper/preprint/database record from a contextual
 * collection, agency, or explanatory page. */
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const entries = JSON.parse(fs.readFileSync(path.join(root, 'journal-index.json'), 'utf8'));
const directHosts = ['nature.com', 'science.org', 'sciencemag.org', 'pnas.org', 'plos.org', 'elifesciences.org', 'frontiersin.org', 'royalsocietypublishing.org', 'onlinelibrary.wiley.com', 'journals.aps.org', 'journals.sagepub.com', 'cambridge.org', 'tandfonline.com', 'springer.com', 'link.springer.com', 'scielo.org', 'jstage.jst.go.jp', 'copernicus.org', 'annualreviews.org', 'academic.oup.com'];
function researchText(entry) { return [entry.title, entry.excerpt, ...(entry.topics || [])].join(' ').toLowerCase(); }
function isResearch(entry) { return (entry.topics || []).includes('Research & Ideas') || /desert|sonoran|mesa|arizona|saguaro|brain|visual|memory|neuron|perception|plant|animal|bacteria|cell|protein|evolution|entropy|information|resonance|archive|record|trace|fossil/.test(researchText(entry)); }
function sourceLink(entry) {
  const file = path.join(root, entry.url);
  if (!fs.existsSync(file)) return '';
  const match = fs.readFileSync(file, 'utf8').match(/<p id="entry-links">[\s\S]*?<a href="([^"]+)"/i);
  return match ? match[1].replace(/&amp;/g, '&') : '';
}
function kindFor(url) {
  try {
    const host = new URL(url).hostname.replace(/^www\./, '');
    if (host === 'doi.org' || host === 'pubmed.ncbi.nlm.nih.gov' || host === 'arxiv.org' || directHosts.some(domain => host === domain || host.endsWith('.' + domain))) return 'direct-study';
  } catch (_) { return 'context-source'; }
  return 'context-source';
}
const sources = entries.filter(isResearch).flatMap(entry => {
  const url = sourceLink(entry);
  return url ? [{ entry: entry.num, kind: kindFor(url) }] : [];
});
fs.writeFileSync(path.join(root, 'reading-sources.json'), JSON.stringify(sources, null, 2) + '\n');
console.log('Wrote ' + sources.length + ' reading source-path records.');
