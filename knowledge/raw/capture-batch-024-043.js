const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = process.cwd();
const BESTBLOGS = 'https://www.bestblogs.dev';
const START_ID = 24;
const TARGET_SUCCESSES = 20;
const OPENCLI_JS = process.env.OPENCLI_JS || 'E:\\yuyan\\npm-global\\node_modules\\@jackwener\\opencli\\dist\\src\\main.js';

const candidates = [
  { href: '/article/048d846e', title: '长时间运行的智能体', topic: '03-control-loop', blocks: 'Control Loop, Context/State, Evaluation', sourceHint: 'BestBlogs / Elevate' },
  { href: '/video/12c8ff4', title: 'OpenAI Greg Brockman：为什么人类注意力会成为新的瓶颈', topic: '06-frontier-radar', blocks: 'Model, Frontier Radar, Product Workflow', sourceHint: 'BestBlogs / Knowledge Project' },
  { href: '/article/483aa7df', title: 'DeepSeek 识图模式是个新模型？！一手实测在此', topic: '06-frontier-radar', blocks: 'Model, Multimodal, Evaluation', sourceHint: 'BestBlogs' },
  { href: '/article/bfc8df6e', title: '京东广告大模型实战：GRAM 架构如何在 50ms 内完成生成式推荐？', topic: '06-frontier-radar', blocks: 'Architecture, Model, Product Workflow', sourceHint: 'BestBlogs' },
  { href: '/podcast/3173b05', title: '前字节研究员深度访谈：中国 AI 的真实差距、刷榜文化与 Agent 新赛道', topic: '06-frontier-radar', blocks: 'Frontier Radar, Model, Agent Ecosystem', sourceHint: 'BestBlogs Podcast' },
  { href: '/explore/topics/gpt-5-5-release', title: 'GPT-5.5 发布：OpenAI 把真实工作推向智能体模型', topic: '06-frontier-radar', blocks: 'Model, Tools/Actions, Evaluation', sourceHint: 'BestBlogs Topic' },
  { href: '/explore/topics/deepseek-v4-preview-release', title: 'DeepSeek-V4 预览版发布', topic: '06-frontier-radar', blocks: 'Model, Context/State, Agent Ecosystem', sourceHint: 'BestBlogs Topic' },
  { href: '/explore/topics/claude-opus-4-7-release', title: 'Claude Opus 4.7 发布', topic: '06-frontier-radar', blocks: 'Model, Control Loop, Evaluation', sourceHint: 'BestBlogs Topic' },
  { href: '/explore/topics/andrej-karpathy-profile', title: '一文读懂 Andrej Karpathy：从 OpenAI 到 Software 3.0', topic: '06-frontier-radar', blocks: 'Concept, Context/State, Frontier Radar', sourceHint: 'BestBlogs Topic' },
  { href: '/explore/topics/china-flagship-llm-2026-spring', title: '中国旗舰大模型横评 2026 春', topic: '06-frontier-radar', blocks: 'Model, Evaluation, Agent Ecosystem', sourceHint: 'BestBlogs Topic' },
  { href: '/explore/topics/frontier-llm-2026-spring', title: '前沿大模型横评 2026 春', topic: '06-frontier-radar', blocks: 'Model, Evaluation, Tool Selection', sourceHint: 'BestBlogs Topic' },
  { href: '/explore/topics/boris-cherny-claude-code-profile', title: 'Boris Cherny 与 Claude Code 的诞生', topic: '03-control-loop', blocks: 'Control Loop, Tools/Actions, Product Workflow', sourceHint: 'BestBlogs Topic' },
  { href: '/explore/topics/ai-native-product-teams', title: 'AI 原生产品团队', topic: '03-control-loop', blocks: 'Product Workflow, Control Loop, Deliverable', sourceHint: 'BestBlogs Topic' },
  { href: '/explore/topics/chatgpt-images-2-thinking-image-models', title: 'ChatGPT Images 2.0 与会思考的图像模型', topic: '06-frontier-radar', blocks: 'Model, Multimodal, Product Workflow', sourceHint: 'BestBlogs Topic' },
  { href: '/video/afa3a1f', title: '训练前沿小模型的全部经验', topic: '06-frontier-radar', blocks: 'Model, Evaluation, Frontier Radar', sourceHint: 'BestBlogs Video' },
  { href: '/zh/newsletter/issue92', title: 'BestBlogs.dev 第 92 期：模型周 04-24', topic: '06-frontier-radar', blocks: 'Frontier Radar, Model, Agent Ecosystem', sourceHint: 'BestBlogs Newsletter' },
  { href: '/zh/newsletter/issue91', title: 'BestBlogs.dev 第 91 期：基建周 04-17', topic: '06-frontier-radar', blocks: 'Infrastructure, Tools/Actions, Agent Ecosystem', sourceHint: 'BestBlogs Newsletter' },
  { href: '/zh/newsletter/issue90', title: 'BestBlogs.dev 第 90 期：脑与手 04-10', topic: '03-control-loop', blocks: 'Control Loop, Tools/Actions, Harness Engineering', sourceHint: 'BestBlogs Newsletter' },
  { href: '/zh/newsletter/issue89', title: 'BestBlogs.dev 第 89 期', topic: '06-frontier-radar', blocks: 'Frontier Radar, Agent Ecosystem, Product Workflow', sourceHint: 'BestBlogs Newsletter' },
  { href: '/zh/newsletter/issue85', title: 'BestBlogs.dev 第 85 期', topic: '06-frontier-radar', blocks: 'Frontier Radar, Agent Ecosystem, Product Workflow', sourceHint: 'BestBlogs Newsletter' },
  { href: '/zh/newsletter/issue84', title: 'BestBlogs.dev 第 84 期：编排 02-27', topic: '03-control-loop', blocks: 'Control Loop, Multi-agent, Agentic Engineering', sourceHint: 'BestBlogs Newsletter' },
  { href: '/zh/newsletter/issue83', title: 'BestBlogs.dev 第 83 期', topic: '03-control-loop', blocks: 'AI Coding, Spec-Driven Development, Deliverable', sourceHint: 'BestBlogs Newsletter' },
];

function readUtf8(file) {
  return fs.existsSync(file) ? fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '') : '';
}

function runOpenCli(args) {
  return execFileSync(process.execPath, [OPENCLI_JS, ...args], {
    cwd: ROOT,
    encoding: 'utf8',
    maxBuffer: 100 * 1024 * 1024,
    windowsHide: true,
  });
}

function sleep(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}

function metaValue(data, key) {
  const item = (data.metas || []).find((m) => m.property === key || m.name === key);
  return item && item.content ? item.content : '';
}

function safeTitle(data, fallback) {
  return (metaValue(data, 'og:title') || data.title || fallback || '').replace(/\s*\|\s*BestBlogs\.dev\s*$/i, '').trim();
}

function inferDate(data) {
  const values = [
    metaValue(data, 'article:published_time'),
    metaValue(data, 'datePublished'),
    metaValue(data, 'pubdate'),
    data.content || '',
  ];
  for (const value of values) {
    const match = String(value).match(/\b20\d{2}-\d{2}-\d{2}\b/);
    if (match) return match[0];
  }
  return '2026-05-01';
}

function chooseOriginalLink(data) {
  const links = data.links || [];
  return links.find((l) => /查看原文|原文|Original|Source/i.test(l.text || l.title || ''))
    || links.find((l) => l.href && !l.href.includes('bestblogs.dev'));
}

function firstMeaningfulLinks(data) {
  return (data.links || [])
    .filter((l) => l.href && !l.href.includes('#main-content') && (l.text || l.title))
    .slice(0, 80);
}

function mdEscapeCell(text) {
  return String(text || '').replace(/\|/g, '/').replace(/\r?\n/g, ' ').trim();
}

function writeItemFiles(entry, id, data) {
  const itemDir = path.join(ROOT, 'knowledge', 'items', entry.topic, id);
  const rawDir = path.join(itemDir, 'raw');
  fs.mkdirSync(rawDir, { recursive: true });

  fs.writeFileSync(path.join(rawDir, 'dom-full.json'), `${JSON.stringify(data, null, 2)}\n`, 'utf8');

  const title = safeTitle(data, entry.title);
  const date = inferDate(data);
  const description = metaValue(data, 'description') || metaValue(data, 'og:description') || '';
  const content = data.content || '';
  const original = chooseOriginalLink(data);
  const tags = (data.metas || [])
    .filter((m) => m.property === 'article:tag' || m.name === 'keywords')
    .map((m) => m.content)
    .filter(Boolean);

  const article = [
    `# ${title}`,
    '',
    `- BestBlogs URL: ${data.url}`,
    `- Extraction: DOM text from BestBlogs page`,
    `- Extracted chars: ${content.length}`,
    original ? `- Original publisher URL: ${original.href}` : '- Original publisher URL: Not found on page during capture.',
    '',
    '---',
    '',
    content,
    '',
  ].join('\n');
  fs.writeFileSync(path.join(itemDir, 'article.md'), article, 'utf8');

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
  for (const link of firstMeaningfulLinks(data)) {
    sourceLines.push(`- ${link.text || link.title || link.href}: ${link.href}`);
  }
  sourceLines.push('');
  fs.writeFileSync(path.join(itemDir, 'source.md'), sourceLines.join('\n'), 'utf8');

  const summary = [
    `# ${id} Summary`,
    '',
    '## Article',
    '',
    `- Title: ${title}`,
    `- Source: ${entry.sourceHint}`,
    `- URL: ${data.url}`,
    `- Date: ${date}`,
    `- Topic: \`${entry.topic}\``,
    tags.length ? `- Tags: ${tags.join(', ')}` : '- Tags: ',
    '',
    '## Model Mapping',
    '',
    `- Blocks: ${entry.blocks}`,
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
  ].join('\n');
  fs.writeFileSync(path.join(itemDir, 'summary.md'), summary, 'utf8');

  return {
    id,
    date,
    title,
    source: entry.sourceHint,
    topic: entry.topic,
    blocks: entry.blocks,
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
    index += `\n| ${r.id} | ${mdEscapeCell(r.date)} | ${mdEscapeCell(r.title)} | ${mdEscapeCell(r.source)} | \`${r.topic}\` | ${mdEscapeCell(r.blocks)} | ${mdEscapeCell(r.status)} |`;
  }
  index += '\n';
  fs.writeFileSync(indexPath, index, 'utf8');
}

function nextId(offset) {
  return `BB-2026-05-01-${String(START_ID + offset).padStart(3, '0')}`;
}

function isAlreadyIndexed(url, index) {
  return index.includes(url) || index.includes(url.replace(BESTBLOGS, ''));
}

function capture(entry, id) {
  const url = entry.href.startsWith('http') ? entry.href : `${BESTBLOGS}${entry.href}`;
  const openOutput = runOpenCli(['browser', 'open', url]);
  const opened = JSON.parse(openOutput);
  const tab = opened.page;
  sleep(5500);

  const js = `(() => {
    const root = document.querySelector('#bbArticleContent') || document.querySelector('article') || document.querySelector('main') || document.body;
    return {
      url: location.href,
      title: document.title,
      content: root ? root.innerText : document.body.innerText,
      links: Array.from(document.querySelectorAll('a[href]')).map(a => ({ href: a.href, text: (a.innerText || '').trim(), title: a.title || '' })).filter(x => x.href && (x.text || x.title)).slice(0, 180),
      metas: Array.from(document.querySelectorAll('meta')).map(m => ({ property: m.getAttribute('property'), name: m.getAttribute('name'), content: m.getAttribute('content') })).filter(x => x.content)
    };
  })()`;
  const evalOutput = runOpenCli(['browser', 'eval', js, '--tab', tab]);
  const data = JSON.parse(evalOutput);
  try {
    runOpenCli(['browser', 'tab', 'close', tab]);
  } catch (_) {
    // Closing is best-effort; stale tabs are harmless for capture quality.
  }
  if (!data.content || data.content.length < 200) {
    throw new Error(`Captured content too short: ${data.content ? data.content.length : 0}`);
  }
  return writeItemFiles(entry, id, data);
}

function main() {
  const index = readUtf8(path.join(ROOT, 'knowledge', 'catalog', 'articles-index.md'));
  const results = [];
  const errors = [];
  let idOffset = 0;

  for (const entry of candidates) {
    if (results.filter((r) => r.chars > 800).length >= TARGET_SUCCESSES) break;
    const url = entry.href.startsWith('http') ? entry.href : `${BESTBLOGS}${entry.href}`;
    if (isAlreadyIndexed(url, index)) continue;
    const id = nextId(idOffset++);
    console.log(`[capture] ${id} ${url}`);
    try {
      const result = capture(entry, id);
      results.push(result);
      updateIndex([result]);
      console.log(`[ok] ${id} chars=${result.chars} topic=${result.topic}`);
    } catch (err) {
      errors.push({ id, url, message: err.message });
      console.error(`[fail] ${id} ${err.message}`);
    }
  }

  const report = {
    generatedAt: new Date().toISOString(),
    targetSuccesses: TARGET_SUCCESSES,
    fullTextSuccesses: results.filter((r) => r.chars > 800).length,
    captured: results,
    errors,
  };
  fs.writeFileSync(path.join(ROOT, 'knowledge', 'raw', 'batch-024-043-report.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(report, null, 2));
}

main();
