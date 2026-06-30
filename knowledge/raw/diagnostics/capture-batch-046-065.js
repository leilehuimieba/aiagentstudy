const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = process.cwd();
const BESTBLOGS = 'https://www.bestblogs.dev';
const OPENCLI_JS = process.env.OPENCLI_JS || 'E:\\yuyan\\npm-global\\node_modules\\@jackwener\\opencli\\dist\\src\\main.js';
const START_ID = 46;
const TARGET_CAPTURES = 20;

const candidates = [
  { href: '/article/3a983d15', title: '早报｜苹果：下季度内存成本压力将显著加大/宇树最便宜人形机器发布/5 月 1 日高速车流或创历史纪录', topic: '06-frontier-radar', blocks: 'Model, Product Workflow, Ecosystem', sourceHint: 'BestBlogs / 爱范儿' },
  { href: '/article/4fad6520', title: '2026-05-01 Hacker News Top Stories #', topic: '04-evaluation-guardrails', blocks: 'Evaluation, Guardrails, Ecosystem', sourceHint: 'BestBlogs / SuperTechFans' },
  { href: '/article/5de75aba', title: 'Codex CLI 0.128.0 新增 /goal 命令', topic: '03-control-loop', blocks: 'Control Loop, Tools/Actions, Evaluation', sourceHint: "BestBlogs / Simon Willison's Weblog" },
  { href: '/article/29a3b9f4', title: '我们对 OpenAI GPT-5.5 网络能力的评估', topic: '04-evaluation-guardrails', blocks: 'Evaluation, Guardrails, Model', sourceHint: "BestBlogs / Simon Willison's Weblog" },
  { href: '/article/4423e7bb', title: 'Meta 解雇举报用户隐私的承包商', topic: '04-evaluation-guardrails', blocks: 'Evaluation, Guardrails, Ethics', sourceHint: 'BestBlogs / Ars Technica' },
  { href: '/article/c517725e', title: '被色彩理论难住的 GenAI', topic: '04-evaluation-guardrails', blocks: 'Evaluation, Tools/Actions, Context/State', sourceHint: 'BestBlogs / UX Collective' },
  { href: '/podcast/4de58ea', title: '139. 【Agent 的综述】和苏煜聊 Agent 技术史、OpenClaw Moment、边界的消弭和社会的辐射', topic: '03-control-loop', blocks: 'Control Loop, Model, Memory', sourceHint: 'BestBlogs / 张小珺Jùn｜商业访谈录' },
  { href: '/podcast/8841f9c', title: '#516. Andrej Karpathy 对谈：为什么程序员从未如此落后？', topic: '03-control-loop', blocks: 'Control Loop, Evaluation, Engineering Culture', sourceHint: 'BestBlogs / 跨国串门儿计划' },
  { href: '/podcast/2c63ae8', title: '#515. GPT-5、Claude 和 Gemini 的是如何训练与部署的', topic: '06-frontier-radar', blocks: 'Model, Evaluation, Infrastructure', sourceHint: 'BestBlogs / 跨国串门儿计划' },
  { href: '/podcast/d87654c', title: '#514.DeepMind 创始人 Demis Hassabis 谈 AGI、AlphaFold 与科学发现的未来', topic: '06-frontier-radar', blocks: 'Model, Context/State, Infrastructure', sourceHint: 'BestBlogs / 跨国串门儿计划' },
  { href: '/podcast/386d82f', title: '163: 详解 DeepSeek V4：Infra 巨鲸、百万上下文走进现实、极致效率优化', topic: '06-frontier-radar', blocks: 'Model, Control Loop, Product Workflow', sourceHint: 'BestBlogs / 晚点聊 LateTalk' },
  { href: '/video/6273638', title: 'Codex 为 Virgin Atlantic 解锁了什么', topic: '02-tools-actions', blocks: 'Tools/Actions, Product Workflow, Infrastructure', sourceHint: 'BestBlogs / OpenAI' },
  { href: '/video/7b97f9e', title: 'AssemblyAI 2026 年 4 月产品更新回顾', topic: '02-tools-actions', blocks: 'Tools/Actions, Evaluation, Infrastructure', sourceHint: 'BestBlogs / AssemblyAI' },
  { href: '/video/ae97639', title: 'Magnific CEO Joaquín Cuenca Abela 谈 AI 视频营销', topic: '06-frontier-radar', blocks: 'Product Workflow, Growth, Infrastructure', sourceHint: 'BestBlogs / This Week in Startups' },
  { href: '/video/607611e', title: 'Claude Design 隐藏 Tweaks 属性：自定义设计控制面板', topic: '02-tools-actions', blocks: 'Tools/Actions, UI Workflow, Design', sourceHint: 'BestBlogs / DesignerUp' },
  { href: '/video/367df0d', title: 'Claude Code 非技术用户完整指南', topic: '02-tools-actions', blocks: 'Tools/Actions, Onboarding, Product Workflow', sourceHint: 'BestBlogs / Futurepedia' },
  { href: '/video/6e2d3a8', title: '100 天完成 100 年进展：Sequoia AI Ascent 2026 Keynote', topic: '06-frontier-radar', blocks: 'Model, Control Loop, Product Workflow', sourceHint: 'BestBlogs / Sequoia Capital' },
  { href: '/video/297a3b9', title: 'GitHub 2026 可靠性危机：故障、AI agents 与开发者信任', topic: '04-evaluation-guardrails', blocks: 'Evaluation, Guardrails, Infrastructure', sourceHint: 'BestBlogs / Fireship' },
  { href: '/video/f787338', title: '用 Gemini 构建 Conversational Agents：Interactions API 与 Live API', topic: '02-tools-actions', blocks: 'Tools/Actions, Model, Context/State', sourceHint: 'BestBlogs / AI Engineer' },
  { href: '/video/24a0aee', title: '「我不行」：在 AGI 时代重新理解工程师价值', topic: '03-control-loop', blocks: 'Control Loop, Evaluation, Engineering Culture', sourceHint: 'BestBlogs / The PrimeTime' },
];

function runOpenCli(args) {
  return execFileSync(process.execPath, [OPENCLI_JS, ...args], {
    cwd: ROOT,
    encoding: 'utf8',
    maxBuffer: 120 * 1024 * 1024,
    windowsHide: true,
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

function metaValue(data, key) {
  const item = (data.metas || []).find((m) => m.property === key || m.name === key);
  return item && item.content ? item.content : '';
}

function safeTitle(data, fallback) {
  return (metaValue(data, 'og:title') || data.title || fallback || '').replace(/\s*\|\s*BestBlogs\.dev\s*$/i, '').trim();
}

function inferDate(data) {
  const values = [metaValue(data, 'article:published_time'), metaValue(data, 'datePublished'), data.content || ''];
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
  return (data.links || []).filter((l) => l.href && !l.href.includes('#main-content') && (l.text || l.title)).slice(0, 80);
}

function mdCell(text) {
  return String(text || '').replace(/\|/g, '/').replace(/\r?\n/g, ' ').trim();
}

function writeItemFiles(entry, id, data) {
  const itemDir = path.join(ROOT, 'knowledge', 'items', entry.topic, id);
  const rawDir = path.join(itemDir, 'raw');
  fs.mkdirSync(rawDir, { recursive: true });
  writeUtf8(path.join(rawDir, 'dom-full.json'), `${JSON.stringify(data, null, 2)}\n`);

  const title = safeTitle(data, entry.title);
  const date = inferDate(data);
  const description = metaValue(data, 'description') || metaValue(data, 'og:description') || '';
  const content = data.content || '';
  const original = chooseOriginalLink(data);
  const tags = (data.metas || [])
    .filter((m) => m.property === 'article:tag' || m.name === 'keywords')
    .map((m) => m.content)
    .filter(Boolean);

  writeUtf8(path.join(itemDir, 'article.md'), [
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
  writeUtf8(path.join(itemDir, 'summary.md'), summary);

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
    index += `\n| ${r.id} | ${mdCell(r.date)} | ${mdCell(r.title)} | ${mdCell(r.source)} | \`${r.topic}\` | ${mdCell(r.blocks)} | ${mdCell(r.status)} |`;
  }
  index += '\n';
  writeUtf8(indexPath, index);
}

function capture(entry, id) {
  const url = entry.href.startsWith('http') ? entry.href : `${BESTBLOGS}${entry.href}`;
  const openOutput = runOpenCli(['browser', 'open', url]);
  const opened = JSON.parse(openOutput);
  const tab = opened.page;
  sleep(4500);

  const js = `(() => {\n    const root = document.querySelector('#bbArticleContent') || document.querySelector('article') || document.querySelector('main') || document.body;\n    return {\n      url: location.href,\n      title: document.title,\n      content: root ? root.innerText : document.body.innerText,\n      links: Array.from(document.querySelectorAll('a[href]')).map(a => ({ href: a.href, text: (a.innerText || '').trim(), title: a.title || '' })).filter(x => x.href && (x.text || x.title)).slice(0, 180),\n      metas: Array.from(document.querySelectorAll('meta')).map(m => ({ property: m.getAttribute('property'), name: m.getAttribute('name'), content: m.getAttribute('content') })).filter(x => x.content)\n    };\n  })()`;
  const evalOutput = runOpenCli(['browser', 'eval', js, '--tab', tab]);
  const data = JSON.parse(evalOutput);
  try { runOpenCli(['browser', 'tab', 'close', tab]); } catch (_) {}
  if (!data.content || data.content.length < 80) throw new Error(`Captured content too short: ${data.content ? data.content.length : 0}`);
  return writeItemFiles(entry, id, data);
}

function main() {
  const index = readUtf8(path.join(ROOT, 'knowledge', 'catalog', 'articles-index.md'));
  const results = [];
  const errors = [];
  let offset = 0;

  for (const entry of candidates) {
    if (results.length >= TARGET_CAPTURES) break;
    const url = entry.href.startsWith('http') ? entry.href : `${BESTBLOGS}${entry.href}`;
    if (index.includes(url)) continue;
    const id = `BB-2026-05-01-${String(START_ID + offset++).padStart(3, '0')}`;
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
    targetCaptures: TARGET_CAPTURES,
    captured: results,
    errors,
  };
  writeUtf8(path.join(ROOT, 'knowledge', 'raw', 'batch-046-065-report.json'), `${JSON.stringify(report, null, 2)}\n`);
  console.log(JSON.stringify(report, null, 2));
}

main();
