const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = process.cwd();
const BESTBLOGS = 'https://www.bestblogs.dev';
const OPENCLI_JS = process.env.OPENCLI_JS || 'D:\\newwork\\opencli\\dist\\src\\main.js';
const TARGET_CAPTURES = Number(process.env.TARGET_CAPTURES || 10);
const OPENCLI_TIMEOUT_MS = Number(process.env.OPENCLI_TIMEOUT_MS || 60000);
const LIVE_CANDIDATES = process.env.CANDIDATES_FILE
  ? path.resolve(ROOT, process.env.CANDIDATES_FILE)
  : path.join(ROOT, 'knowledge', 'raw', 'latest-articles-candidates-live.json');

function runOpenCli(args) {
  return execFileSync(process.execPath, [OPENCLI_JS, ...args], {
    cwd: ROOT,
    encoding: 'utf8',
    maxBuffer: 160 * 1024 * 1024,
    windowsHide: true,
    timeout: OPENCLI_TIMEOUT_MS,
  });
}

function sleep(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}

function readUtf8(file) {
  return fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
}

function writeUtf8(file, text) {
  fs.writeFileSync(file, text, 'utf8');
}

function normalizeBestBlogsUrl(url) {
  return String(url || '')
    .replace('https://www.bestblogs.dev/en/', 'https://www.bestblogs.dev/')
    .replace(/[?#].*/, '');
}

function walk(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}

function existingBestBlogsUrls() {
  const urls = new Set();
  for (const file of walk(path.join(ROOT, 'knowledge', 'items')).filter((p) => path.basename(p) === 'source.md')) {
    const text = readUtf8(file);
    const main = text.match(/^- BestBlogs URL:\s*(https:\/\/www\.bestblogs\.dev\/(?:en\/)?(?:article|video|podcast|status|explore\/topics)\/[^\s]+)\s*$/m);
    if (main) urls.add(normalizeBestBlogsUrl(main[1]));
  }
  return urls;
}

function nextIdBase() {
  const index = readUtf8(path.join(ROOT, 'knowledge', 'catalog', 'articles-index.md'));
  let max = 0;
  for (const match of index.matchAll(/BB-2026-05-01-(\d{3})/g)) {
    max = Math.max(max, Number(match[1]));
  }
  return max + 1;
}

function metaValue(data, key) {
  const item = (data.metas || []).find((m) => m.property === key || m.name === key);
  return item && item.content ? item.content : '';
}

function safeTitle(data, fallback) {
  return (metaValue(data, 'og:title') || data.title || fallback || '')
    .replace(/\s*\|\s*BestBlogs\.dev\s*$/i, '')
    .trim();
}

function inferDate(data) {
  const values = [
    metaValue(data, 'article:published_time'),
    metaValue(data, 'datePublished'),
    data.content || '',
  ];
  for (const value of values) {
    const match = String(value).match(/\b20\d{2}-\d{2}-\d{2}\b/);
    if (match) return match[0];
  }
  return '2026-05-05';
}

function chooseOriginalLink(data) {
  const links = data.links || [];
  return links.find((l) => l.href && !l.href.includes('bestblogs.dev') && /View Source|查看原文|原文|Original|Source/i.test(l.text || l.title || ''))
    || links.find((l) => l.href && !l.href.includes('bestblogs.dev'));
}

function firstMeaningfulLinks(data) {
  return (data.links || [])
    .filter((l) => l.href && !l.href.includes('#main-content') && (l.text || l.title))
    .slice(0, 90);
}

function mdCell(text) {
  return String(text || '').replace(/\|/g, '/').replace(/\r?\n/g, ' ').trim();
}

function inferTopicAndBlocks(title, url, content) {
  const hay = `${title}\n${url}\n${content.slice(0, 2000)}`.toLowerCase();
  if (/memory|context|rag|上下文|记忆|检索/.test(hay)) {
    return { topic: '01-context-memory', blocks: 'Context/State, Memory, Tools/Actions' };
  }
  if (/tool|mcp|cli|codex|claude code|gemini|api|websocket|agent.*tool|工具|接口/.test(hay)) {
    return { topic: '02-tools-actions', blocks: 'Tools/Actions, Control Loop, Deliverable' };
  }
  if (/reliab|eval|guard|sandbox|安全|评估|审查|ci|测试/.test(hay)) {
    return { topic: '04-evaluation-guardrails', blocks: 'Evaluation, Guardrails, Tools/Actions' };
  }
  if (/agent|harness|workflow|software|developer|coding|编程|研发|工程|开发/.test(hay)) {
    return { topic: '03-control-loop', blocks: 'Goal, Control Loop, Tools/Actions, Evaluation' };
  }
  return { topic: '06-frontier-radar', blocks: 'Model, Frontier Radar, Product Workflow' };
}

function sourceHintFromData(data, fallback) {
  const links = data.links || [];
  const source = links.find((l) => l.href && /bestblogs\.dev\/(?:articles|videos|podcasts)\?source/i.test(l.href));
  return source && (source.text || source.title)
    ? `BestBlogs / ${source.text || source.title}`
    : fallback || 'BestBlogs';
}

function writeItemFiles(entry, id, data) {
  const title = safeTitle(data, entry.title);
  const date = inferDate(data);
  const content = data.content || '';
  const original = chooseOriginalLink(data);
  const topicInfo = inferTopicAndBlocks(title, data.url, content);
  const sourceHint = sourceHintFromData(data, entry.sourceHint);
  const description = metaValue(data, 'description') || metaValue(data, 'og:description') || '';
  const tags = (data.metas || [])
    .filter((m) => m.property === 'article:tag' || m.name === 'keywords')
    .map((m) => m.content)
    .filter(Boolean);

  const itemDir = path.join(ROOT, 'knowledge', 'items', topicInfo.topic, id);
  const rawDir = path.join(itemDir, 'raw');
  fs.mkdirSync(rawDir, { recursive: true });
  writeUtf8(path.join(rawDir, 'dom-full.json'), `${JSON.stringify(data, null, 2)}\n`);

  writeUtf8(path.join(itemDir, 'article.md'), [
    `# ${title}`,
    '',
    `- BestBlogs URL: ${data.url}`,
    '- Extraction: DOM text from BestBlogs page via OpenCLI browser bridge',
    `- Extracted chars: ${content.length}`,
    original ? `- Original publisher URL: ${original.href}` : '- Original publisher URL: Not found on page during capture.',
    '',
    '---',
    '',
    content,
    '',
  ].join('\n'));

  const sourceLines = [
    '# Source Evidence',
    '',
    `- Title: ${title}`,
    `- BestBlogs URL: ${data.url}`,
    `- Original publisher URL: ${original ? original.href : 'Not found on page during capture.'}`,
  ];
  if (original) sourceLines.push(`- Original link text: ${original.text || original.title || ''}`);
  sourceLines.push('', '## Captured Page Metadata', '', `- Browser title: ${data.title || ''}`, `- Description: ${description || ''}`, `- Date: ${date}`, '');
  sourceLines.push('## Evidence Links Captured', '');
  for (const link of firstMeaningfulLinks(data)) sourceLines.push(`- ${link.text || link.title || link.href}: ${link.href}`);
  sourceLines.push('');
  writeUtf8(path.join(itemDir, 'source.md'), sourceLines.join('\n'));

  writeUtf8(path.join(itemDir, 'summary.md'), [
    `# ${id} Summary`,
    '',
    '## Article',
    '',
    `- Title: ${title}`,
    `- Source: ${sourceHint}`,
    `- URL: ${data.url}`,
    `- Date: ${date}`,
    `- Topic: \`${topicInfo.topic}\``,
    tags.length ? `- Tags: ${tags.join(', ')}` : '- Tags: ',
    '',
    '## Model Mapping',
    '',
    `- Blocks: ${topicInfo.blocks}`,
    '- Layer: captured frontier material, pending deep reading',
    '',
    '## Core Takeaway',
    '',
    description || 'Full text captured for later selective reading and synthesis.',
    '',
    '## Reusable Principle',
    '',
    'Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.',
    '',
  ].join('\n'));

  return {
    id,
    date,
    title,
    source: sourceHint,
    topic: topicInfo.topic,
    blocks: topicInfo.blocks,
    status: content.length > 800 ? 'Full text + source captured' : 'Short page captured',
    chars: content.length,
    original: original ? original.href : '',
    dir: path.relative(ROOT, itemDir),
  };
}

function updateIndex(results) {
  const indexPath = path.join(ROOT, 'knowledge', 'catalog', 'articles-index.md');
  let index = readUtf8(indexPath).trimEnd();
  for (const r of results) {
    if (index.includes(r.id)) continue;
    index += `\n| ${r.id} | ${mdCell(r.date)} | ${mdCell(r.title)} | ${mdCell(r.source)} | \`${r.topic}\` | ${mdCell(r.blocks)} | ${mdCell(r.status)} |`;
  }
  index += '\n';
  writeUtf8(indexPath, index);
}

function capture(entry, id) {
  const url = entry.url || (entry.href.startsWith('http') ? entry.href : `${BESTBLOGS}${entry.href}`);
  const openOutput = runOpenCli(['browser', 'open', url]);
  const opened = JSON.parse(openOutput);
  const tab = opened.page;
  sleep(6500);

  const js = `(() => {
    const root = document.querySelector('#bbArticleContent') || document.querySelector('article') || document.querySelector('main') || document.body;
    return {
      url: location.href,
      title: document.title,
      content: root ? root.innerText : document.body.innerText,
      links: Array.from(document.querySelectorAll('a[href]')).map(a => ({ href: a.href, text: (a.innerText || '').trim(), title: a.title || '' })).filter(x => x.href && (x.text || x.title)).slice(0, 220),
      metas: Array.from(document.querySelectorAll('meta')).map(m => ({ property: m.getAttribute('property'), name: m.getAttribute('name'), content: m.getAttribute('content') })).filter(x => x.content)
    };
  })()`;
  const evalOutput = runOpenCli(['browser', 'eval', js, '--tab', tab]);
  const data = JSON.parse(evalOutput);
  try { runOpenCli(['browser', 'tab', 'close', tab]); } catch (_) {}
  if (!data.content || data.content.length < 80) throw new Error(`Captured content too short: ${data.content ? data.content.length : 0}`);
  if (/欢迎来到 BestBlogs|登录/.test(data.title || '') && !/article|podcast|video|status/i.test(data.title || '')) {
    throw new Error(`Captured non-article page: ${data.title || ''}`);
  }
  if (/欢迎来到 BestBlogs[\s\S]{0,200}(登录|免费开始|跳转到主要内容)/.test(data.content || '')) {
    throw new Error(`Captured BestBlogs welcome/login page instead of item content: ${data.content.length}`);
  }
  return writeItemFiles(entry, id, data);
}

function chooseCandidates() {
  const live = JSON.parse(readUtf8(LIVE_CANDIDATES));
  const existing = existingBestBlogsUrls();
  const seen = new Set();
  return (live.cards || [])
    .map((c) => ({
      url: normalizeBestBlogsUrl(c.href || c.url),
      title: c.text || '',
      sourceHint: 'BestBlogs',
    }))
    .filter((c) => c.url)
    .filter((c) => !existing.has(c.url))
    .filter((c) => {
      if (seen.has(c.url)) return false;
      seen.add(c.url);
      return true;
    });
}

function main() {
  const candidates = chooseCandidates();
  const results = [];
  const errors = [];
  const start = nextIdBase();

  for (const entry of candidates) {
    if (results.length >= TARGET_CAPTURES) break;
    const id = `BB-2026-05-01-${String(start + results.length).padStart(3, '0')}`;
    console.log(`[capture] ${id} ${entry.url}`);
    try {
      const result = capture(entry, id);
      results.push(result);
      updateIndex([result]);
      console.log(`[ok] ${id} chars=${result.chars} topic=${result.topic}`);
    } catch (err) {
      errors.push({ plannedId: id, url: entry.url, title: entry.title, message: err.message });
      console.error(`[fail] ${id} ${err.message}`);
    }
  }

  const report = {
    generatedAt: new Date().toISOString(),
    targetCaptures: TARGET_CAPTURES,
    captured: results,
    errors,
  };
  const firstId = results[0] ? results[0].id.replace('BB-2026-05-01-', '') : String(start).padStart(3, '0');
  const lastId = results[results.length - 1] ? results[results.length - 1].id.replace('BB-2026-05-01-', '') : String(start + TARGET_CAPTURES - 1).padStart(3, '0');
  writeUtf8(path.join(ROOT, 'knowledge', 'raw', `batch-${firstId}-${lastId}-report.json`), `${JSON.stringify(report, null, 2)}\n`);
  console.log(JSON.stringify(report, null, 2));
  if (results.length < TARGET_CAPTURES) process.exitCode = 2;
}

main();
