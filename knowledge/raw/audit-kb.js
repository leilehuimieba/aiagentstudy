const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const itemsRoot = path.join(root, 'items');
const indexPath = path.join(root, 'catalog', 'articles-index.md');
const candidatesRoot = path.join(root, 'candidates');
const articleLengthOverridesPath = path.join(root, 'quality', 'article-length-overrides.json');

function read(file) {
  return fs.readFileSync(file, 'utf8');
}

function listItemDirs() {
  const dirs = [];
  function walk(dir) {
    const summaryPath = path.join(dir, 'summary.md');
    const articlePath = path.join(dir, 'article.md');
    const sourcePath = path.join(dir, 'source.md');
    if (fs.existsSync(summaryPath) || fs.existsSync(articlePath) || fs.existsSync(sourcePath)) {
      dirs.push(dir);
      return;
    }
    for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
      if (item.isDirectory()) walk(path.join(dir, item.name));
    }
  }
  for (const topic of fs.readdirSync(itemsRoot, { withFileTypes: true })) {
    if (topic.isDirectory()) walk(path.join(itemsRoot, topic.name));
  }
  return dirs.sort();
}

function parseIndex() {
  const map = new Map();
  const counts = new Map();
  for (const line of read(indexPath).split(/\r?\n/)) {
    if (!line.startsWith('| ')) continue;
    const parts = line.split('|').map((part) => part.trim());
    if (parts.length < 8 || !/^[A-Z][A-Z0-9-]+-\d{4}/.test(parts[1])) continue;
    counts.set(parts[1], (counts.get(parts[1]) || 0) + 1);
    map.set(parts[1], {
      title: parts[3],
      source: parts[4],
      topic: parts[5],
      blocks: parts[6],
      status: parts[7],
      rawLine: line,
    });
  }
  return {
    map,
    duplicateIds: [...counts.entries()]
      .filter(([, count]) => count > 1)
      .map(([id, count]) => ({ id, count })),
  };
}

function extractUrls(text) {
  return [...text.matchAll(/https?:\/\/[^\s)]+/g)].map((match) => match[0]);
}

function hasPlaceholderLoss(text) {
  return /\?{3,}/.test(text);
}

function summaryFields(summaryText) {
  const title = summaryText.match(/^- Title: (.+)$/m)?.[1] || '';
  const source = summaryText.match(/^- Source: (.+)$/m)?.[1] || '';
  const url = summaryText.match(/^- URL: (.+)$/m)?.[1] || '';
  return { title, source, url };
}

function normalizeUrl(url) {
  try {
    const parsed = new URL(url);
    parsed.hash = '';
    parsed.search = '';
    return parsed.toString().replace(/\/$/, '');
  } catch {
    return '';
  }
}

function loadItemJson(itemJsonPath, id, report) {
  if (!fs.existsSync(itemJsonPath)) {
    report.missing.itemJson.push(id);
    return null;
  }
  try {
    const itemJson = JSON.parse(read(itemJsonPath));
    if (itemJson.id !== id) report.invalid.itemJson.push({ id, error: `id mismatch: ${itemJson.id}` });
    return itemJson;
  } catch (error) {
    report.invalid.itemJson.push({ id, error: error.message });
    return null;
  }
}

function itemUrls(itemJson) {
  const urls = [];
  const values = (itemJson && itemJson.urls) || {};
  for (const key of ['source_url', 'original_url', 'requested_url', 'feed_url', 'pdf_url', 'candidate_url']) {
    if (values[key]) urls.push(values[key]);
  }
  if (Array.isArray(values.all_source_urls)) urls.push(...values.all_source_urls);
  return urls.filter(Boolean);
}

function isBestBlogsItem(itemJson, sourceUrls) {
  if (!itemJson) return false;
  return itemJson.source_id === 'bestblogs'
    || itemJson.type === 'bestblogs_item'
    || sourceUrls.some((url) => /bestblogs\.dev/.test(url));
}

function loadArticleLengthOverrides() {
  if (!fs.existsSync(articleLengthOverridesPath)) {
    return { accepted: {}, errors: [{ file: articleLengthOverridesPath, error: 'missing file' }] };
  }
  try {
    const data = JSON.parse(read(articleLengthOverridesPath));
    const accepted = data.accepted_short_articles || {};
    return { accepted, errors: [] };
  } catch (error) {
    return { accepted: {}, errors: [{ file: articleLengthOverridesPath, error: error.message }] };
  }
}

function readJsonl(file) {
  if (!fs.existsSync(file)) return { rows: [], errors: [{ file, error: 'missing file' }] };
  const rows = [];
  const errors = [];
  read(file).split(/\r?\n/).forEach((line, idx) => {
    const trimmed = line.trim();
    if (!trimmed) return;
    try {
      rows.push(JSON.parse(trimmed));
    } catch (error) {
      errors.push({ file, line: idx + 1, error: error.message });
    }
  });
  return { rows, errors };
}

function auditCandidates() {
  const files = ['inbox.jsonl', 'promoted.jsonl', 'deferred.jsonl', 'rejected.jsonl'];
  const required = ['candidate_id', 'status', 'type', 'title', 'url', 'source_id', 'discovered_at', 'route'];
  const report = { files: {}, errors: [] };
  const ids = new Set();
  const urls = new Set();

  for (const name of files) {
    const file = path.join(candidatesRoot, name);
    const { rows, errors } = readJsonl(file);
    report.files[name] = rows.length;
    report.errors.push(...errors);
    rows.forEach((row, idx) => {
      for (const field of required) {
        if (!row[field]) report.errors.push({ file: name, line: idx + 1, error: `missing ${field}` });
      }
      if (ids.has(row.candidate_id)) report.errors.push({ file: name, line: idx + 1, error: `duplicate candidate_id ${row.candidate_id}` });
      if (row.candidate_id) ids.add(row.candidate_id);
      const normalized = normalizeUrl(row.url || '');
      if (!normalized) {
        report.errors.push({ file: name, line: idx + 1, error: 'invalid url' });
      } else if (urls.has(normalized)) {
        report.errors.push({ file: name, line: idx + 1, error: `duplicate url ${normalized}` });
      } else {
        urls.add(normalized);
      }
    });
  }
  report.errorCount = report.errors.length;
  return report;
}

function summarizeMismatch(id, indexRow, summaryRow) {
  const notes = [];
  if (summaryRow.title !== indexRow.title) {
    if (hasPlaceholderLoss(summaryRow.title)) {
      notes.push('summary title contains placeholder loss');
    } else {
      notes.push('summary title differs from index title');
    }
  }
  if (summaryRow.source !== indexRow.source) {
    if (/^BestBlogs \/ [A-Z]$/.test(summaryRow.source)) {
      notes.push('summary source looks truncated');
    } else {
      notes.push('summary source differs from index source');
    }
  }
  return { id, notes, indexTitle: indexRow.title, summaryTitle: summaryRow.title, indexSource: indexRow.source, summarySource: summaryRow.source };
}

const indexParse = parseIndex();
const indexMap = indexParse.map;
const itemDirs = listItemDirs();
const articleLengthOverrides = loadArticleLengthOverrides();
const seenArticleLengthOverrides = new Set();

const report = {
  totals: {
    items: itemDirs.length,
    indexRows: indexMap.size,
  },
  missing: {
    itemJson: [],
    summary: [],
    article: [],
    source: [],
    rawDir: [],
    emptyRawDir: [],
  },
  invalid: {
    itemJson: [],
  },
  size: {
    articleUnder800: [],
    articleUnder800Accepted: [],
  },
  quality: {
    articleLengthOverrideErrors: articleLengthOverrides.errors,
    unusedArticleLengthOverrides: [],
  },
  sourceIssues: {
    missingBestBlogsUrl: [],
    missingExternalOriginalUrl: [],
    bestBlogsAsOriginalUrl: [],
  },
  placeholderLoss: {
    summary: [],
    source: [],
    article: [],
    index: [],
  },
  retrievalSurface: {
    duplicateIndexIds: indexParse.duplicateIds,
    summaryVsIndexMismatches: [],
  },
  candidates: auditCandidates(),
};

for (const dir of itemDirs) {
  const id = path.basename(dir);
  const itemJsonPath = path.join(dir, 'item.json');
  const summaryPath = path.join(dir, 'summary.md');
  const articlePath = path.join(dir, 'article.md');
  const sourcePath = path.join(dir, 'source.md');
  const rawDir = path.join(dir, 'raw');

  const itemJson = loadItemJson(itemJsonPath, id, report);

  if (!fs.existsSync(summaryPath)) report.missing.summary.push(id);
  if (!fs.existsSync(articlePath)) report.missing.article.push(id);
  if (!fs.existsSync(sourcePath)) report.missing.source.push(id);
  if (!fs.existsSync(rawDir) || !fs.statSync(rawDir).isDirectory()) {
    report.missing.rawDir.push(id);
  } else if (fs.readdirSync(rawDir).length === 0) {
    report.missing.emptyRawDir.push(id);
  }

  if (fs.existsSync(articlePath)) {
    const size = fs.statSync(articlePath).size;
    if (size <= 800) {
      const override = articleLengthOverrides.accepted[id];
      if (override) {
        seenArticleLengthOverrides.add(id);
        report.size.articleUnder800Accepted.push({
          id,
          size,
          reason: override.reason || '',
          note: override.note || '',
        });
      } else {
        report.size.articleUnder800.push({ id, size });
      }
    }
    const articleText = read(articlePath);
    if (hasPlaceholderLoss(articleText)) report.placeholderLoss.article.push(id);
  }

  if (fs.existsSync(summaryPath)) {
    const summaryText = read(summaryPath);
    if (hasPlaceholderLoss(summaryText)) report.placeholderLoss.summary.push(id);
    const indexRow = indexMap.get(id);
    if (indexRow) {
      const fields = summaryFields(summaryText);
      if (fields.title !== indexRow.title || fields.source !== indexRow.source) {
        report.retrievalSurface.summaryVsIndexMismatches.push(
          summarizeMismatch(id, indexRow, fields),
        );
      }
    }
  }

  if (fs.existsSync(sourcePath)) {
    const sourceText = read(sourcePath);
    const urls = [...new Set([...extractUrls(sourceText), ...itemUrls(itemJson)])];
    const bestBlogsUrls = urls.filter((url) => url.includes('bestblogs.dev'));
    const externalUrls = urls.filter((url) => !url.includes('bestblogs.dev'));
    const bestBlogsItem = isBestBlogsItem(itemJson, urls);
    if (bestBlogsItem && bestBlogsUrls.length === 0) report.sourceIssues.missingBestBlogsUrl.push(id);
    if (bestBlogsItem && externalUrls.length === 0) report.sourceIssues.missingExternalOriginalUrl.push(id);
    const originalLine = sourceText.match(/^- Original publisher URL: (.+)$/m)?.[1] || '';
    if (/bestblogs\.dev/.test(originalLine)) report.sourceIssues.bestBlogsAsOriginalUrl.push(id);
    if (hasPlaceholderLoss(sourceText)) report.placeholderLoss.source.push(id);
  }
}

for (const [id, row] of indexMap.entries()) {
  if (hasPlaceholderLoss(row.rawLine)) report.placeholderLoss.index.push(id);
}

for (const id of Object.keys(articleLengthOverrides.accepted)) {
  if (!seenArticleLengthOverrides.has(id)) report.quality.unusedArticleLengthOverrides.push(id);
}

console.log(JSON.stringify(report, null, 2));
