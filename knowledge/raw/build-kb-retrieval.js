const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const ITEMS_ROOT = path.join(ROOT, 'knowledge', 'items');
const INDEX_PATH = path.join(ROOT, 'knowledge', 'catalog', 'articles-index.md');
const OUT_DIR = path.join(ROOT, 'knowledge', 'retrieval');
const JSON_PATH = path.join(OUT_DIR, 'articles-meta.json');
const JSONL_PATH = path.join(OUT_DIR, 'articles-meta.jsonl');
const REPORT_PATH = path.join(OUT_DIR, 'build-report.json');
const ALIASES_PATH = path.join(OUT_DIR, 'aliases.json');

function read(file) {
  return fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
}

function readJson(file) {
  return JSON.parse(read(file));
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function rel(file) {
  return path.relative(ROOT, file).replace(/\\/g, '/');
}

function parseIndex() {
  const rows = new Map();
  const text = read(INDEX_PATH);
  for (const line of text.split(/\r?\n/)) {
    if (!line.startsWith('| ')) continue;
    const parts = line.split('|').map((part) => part.trim());
    if (parts.length < 8 || !/^[A-Z][A-Z0-9-]+-\d{4}/.test(parts[1])) continue;
    rows.set(parts[1], {
      id: parts[1],
      date: parts[2],
      title: parts[3],
      source: parts[4],
      topic: (parts[5] || '').replace(/`/g, ''),
      blocks: (parts[6] || '').split(',').map((x) => x.trim()).filter(Boolean),
      status: parts[7] || '',
    });
  }
  return rows;
}

function listItemDirs() {
  const dirs = [];
  function walk(dir) {
    const summaryPath = path.join(dir, 'summary.md');
    const articlePath = path.join(dir, 'article.md');
    const sourcePath = path.join(dir, 'source.md');
    if (fs.existsSync(summaryPath) && fs.existsSync(articlePath) && fs.existsSync(sourcePath)) {
      dirs.push(dir);
      return;
    }
    for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
      if (item.isDirectory()) walk(path.join(dir, item.name));
    }
  }
  for (const topic of fs.readdirSync(ITEMS_ROOT, { withFileTypes: true })) {
    if (topic.isDirectory()) walk(path.join(ITEMS_ROOT, topic.name));
  }
  return dirs.sort();
}

function field(text, label) {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return (text.match(new RegExp(`^- ${escaped}:\\s*(.+)$`, 'm')) || [])[1] || '';
}

function sectionBody(text, heading) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = text.match(new RegExp(`^## ${escaped}\\r?\\n\\r?\\n([\\s\\S]*?)(?=\\r?\\n## |$)`, 'm'));
  return match ? match[1].trim() : '';
}

function cleanText(text) {
  return text
    .replace(/\r/g, '')
    .replace(/^#.*$/gm, '')
    .replace(/^- /gm, '')
    .replace(/`/g, '')
    .replace(/\[(.*?)\]\((.*?)\)/g, '$1')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function uniqueList(items) {
  const seen = new Set();
  const out = [];
  for (const item of items) {
    const key = item.trim();
    if (!key || seen.has(key)) continue;
    seen.add(key);
    out.push(key);
  }
  return out;
}

function splitList(value) {
  return uniqueList((value || '').split(',').map((item) => item.trim()));
}

function asList(value) {
  if (Array.isArray(value)) return uniqueList(value.map((item) => String(item || '').trim()));
  if (typeof value === 'string') return splitList(value);
  return [];
}

function asString(value) {
  return typeof value === 'string' ? value.trim() : '';
}

function loadItemMetadata(dir, id, report) {
  const itemJsonPath = path.join(dir, 'item.json');
  if (!fs.existsSync(itemJsonPath)) {
    report.missing_item_json.push(rel(itemJsonPath));
    return null;
  }
  try {
    const metadata = readJson(itemJsonPath);
    if (asString(metadata.id) && asString(metadata.id) !== id) {
      report.invalid_item_json.push({
        path: rel(itemJsonPath),
        reason: `id mismatch: ${metadata.id} != ${id}`,
      });
      return null;
    }
    report.item_json_used += 1;
    return metadata;
  } catch (error) {
    report.invalid_item_json.push({
      path: rel(itemJsonPath),
      reason: error.message,
    });
    return null;
  }
}

function pathFromMetadata(metadata, key, fallback) {
  const value = asString(metadata && metadata.paths && metadata.paths[key]);
  if (!value) return fallback;
  const resolved = path.isAbsolute(value) ? value : path.join(ROOT, value);
  return fs.existsSync(resolved) ? resolved : fallback;
}

function bestblogsUrlFrom(metadata, sourceText, summaryText) {
  const urls = (metadata && metadata.urls) || {};
  const sourceUrl = asString(urls.source_url);
  const allUrls = asList(urls.all_source_urls);
  if (sourceUrl.includes('bestblogs.dev')) return sourceUrl;
  const allBestblogsUrl = allUrls.find((url) => url.includes('bestblogs.dev'));
  if (allBestblogsUrl) return allBestblogsUrl;
  const legacyUrl = field(sourceText, 'BestBlogs URL') || field(summaryText, 'URL');
  return legacyUrl.includes('bestblogs.dev') ? legacyUrl : '';
}

function sourceUrlFrom(metadata, sourceText, bestblogsUrl) {
  const urls = (metadata && metadata.urls) || {};
  return asString(urls.source_url) || field(sourceText, 'Source URL') || bestblogsUrl;
}

function originalUrlFrom(metadata, sourceText, sourceUrl, bestblogsUrl) {
  const urls = (metadata && metadata.urls) || {};
  const originalUrl = asString(urls.original_url) || field(sourceText, 'Original publisher URL');
  if (originalUrl) return originalUrl;
  return sourceUrl && sourceUrl !== bestblogsUrl && !sourceUrl.includes('bestblogs.dev') ? sourceUrl : '';
}

function loadAliases() {
  if (!fs.existsSync(ALIASES_PATH)) return {};
  const aliases = readJson(ALIASES_PATH);
  for (const [id, values] of Object.entries(aliases)) {
    if (!Array.isArray(values)) {
      throw new Error(`Invalid aliases for ${id}: expected an array`);
    }
  }
  return aliases;
}

function articleBody(articleText) {
  const parts = articleText.split(/\r?\n---\r?\n/);
  return (parts[1] || articleText).trim();
}

function excerpt(text, maxChars) {
  return text.replace(/\s+/g, ' ').trim().slice(0, maxChars);
}

const indexRows = parseIndex();
const aliasesById = loadAliases();
const items = [];
const report = {
  item_json_used: 0,
  missing_item_json: [],
  invalid_item_json: [],
};

for (const dir of listItemDirs()) {
  const id = path.basename(dir);
  const index = indexRows.get(id);
  if (!index) continue;

  const metadata = loadItemMetadata(dir, id, report);
  const summaryPath = pathFromMetadata(metadata, 'summary', path.join(dir, 'summary.md'));
  const articlePath = pathFromMetadata(metadata, 'article', path.join(dir, 'article.md'));
  const sourcePath = pathFromMetadata(metadata, 'source', path.join(dir, 'source.md'));
  const rawDir = pathFromMetadata(metadata, 'raw_dir', path.join(dir, 'raw'));

  const summaryText = read(summaryPath);
  const articleText = read(articlePath);
  const sourceText = read(sourcePath);
  const articlePlain = cleanText(articleBody(articleText));
  const summaryPlain = cleanText(summaryText);

  const summaryTitle = asString(metadata && metadata.title) || field(summaryText, 'Title') || index.title;
  const summarySource = asString(metadata && metadata.source) || field(summaryText, 'Source') || index.source;
  const summaryDate = asString(metadata && metadata.date) || field(summaryText, 'Date') || index.date;
  const summaryTopic = (asString(metadata && metadata.topic) || field(summaryText, 'Topic') || index.topic).replace(/`/g, '');
  const bestblogsUrl = bestblogsUrlFrom(metadata, sourceText, summaryText);
  const sourceUrl = sourceUrlFrom(metadata, sourceText, bestblogsUrl);
  const originalUrl = originalUrlFrom(metadata, sourceText, sourceUrl, bestblogsUrl);
  const tags = asList(metadata && metadata.tags).length ? asList(metadata.tags) : splitList(field(summaryText, 'Tags'));
  const aliases = uniqueList(aliasesById[id] || []);
  const blocks = asList(metadata && metadata.blocks).length
    ? asList(metadata.blocks)
    : splitList(field(summaryText, 'Blocks') || index.blocks.join(', '));
  const takeaway = cleanText(sectionBody(summaryText, 'Core Takeaway'));
  const reusable = cleanText(sectionBody(summaryText, 'Reusable Principle'));
  const status = asString(metadata && metadata.status) || index.status;
  const allSourceUrls = asList(metadata && metadata.urls && metadata.urls.all_source_urls);

  items.push({
    id,
    date: summaryDate,
    title: summaryTitle,
    source: summarySource,
    topic: summaryTopic,
    blocks,
    tags,
    aliases,
    status,
    index_title: index.title,
    index_source: index.source,
    source_url: sourceUrl,
    bestblogs_url: bestblogsUrl,
    original_url: originalUrl,
    all_source_urls: allSourceUrls,
    source_id: asString(metadata && metadata.source_id),
    source_name: asString(metadata && metadata.source_name),
    item_type: asString(metadata && metadata.type),
    summary_path: rel(summaryPath),
    article_path: rel(articlePath),
    source_path: rel(sourcePath),
    raw_dir: rel(rawDir),
    summary_text: summaryPlain,
    takeaway,
    reusable_principle: reusable,
    article_preview: excerpt(articlePlain, 1200),
    article_chars: articlePlain.length,
    article_size: fs.statSync(articlePath).size,
    retrieval_text: [
      summaryTitle,
      summarySource,
      summaryTopic,
      blocks.join(', '),
      tags.join(', '),
      aliases.join(', '),
      takeaway,
      reusable,
      excerpt(summaryPlain, 2500),
    ].filter(Boolean).join('\n'),
  });
}

ensureDir(OUT_DIR);
fs.writeFileSync(JSON_PATH, `${JSON.stringify(items, null, 2)}\n`, 'utf8');
fs.writeFileSync(JSONL_PATH, `${items.map((item) => JSON.stringify(item)).join('\n')}\n`, 'utf8');
fs.writeFileSync(REPORT_PATH, `${JSON.stringify({
  generated_at: new Date().toISOString(),
  items: items.length,
  aliases: Object.keys(aliasesById).length,
  item_json_used: report.item_json_used,
  missing_item_json: report.missing_item_json,
  invalid_item_json: report.invalid_item_json,
  outputs: {
    json: rel(JSON_PATH),
    jsonl: rel(JSONL_PATH),
  },
}, null, 2)}\n`, 'utf8');

console.log(JSON.stringify({
  generated_at: new Date().toISOString(),
  items: items.length,
  aliases: Object.keys(aliasesById).length,
  item_json_used: report.item_json_used,
  missing_item_json: report.missing_item_json.length,
  invalid_item_json: report.invalid_item_json.length,
  outputs: {
    json: rel(JSON_PATH),
    jsonl: rel(JSONL_PATH),
    report: rel(REPORT_PATH),
  },
}, null, 2));
