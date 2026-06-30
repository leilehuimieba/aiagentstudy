const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const ITEMS_ROOT = path.join(ROOT, 'knowledge', 'items');
const REPORT = path.join(ROOT, 'knowledge', 'catalog', 'relevance-audit.md');

const strongTerms = [
  'agent', 'agents', 'agentic', '智能体', '代理', 'autonomous',
  'codex', 'claude code', 'claude', 'gemini', 'chatgpt', 'openai',
  'anthropic', 'mcp', 'harness', 'tool', 'tools', '工具',
  'workflow', '工作流', 'coding', '编程', '研发', 'developer',
  'context', '上下文', 'memory', '记忆', 'rag', 'eval', '评估',
  'guardrail', 'sandbox', 'api', 'llm', '大模型', '模型',
  'ai native', 'ai 原生', 'vibe', 'automation', '自动化',
];

const weakOrBroadTerms = [
  'ai', 'agi', 'deepseek', 'gpt', 'sonnet', 'opus', 'software',
  'engineering', '工程', 'product', '产品', 'infrastructure', '基础设施',
  'security', '安全', 'privacy', '隐私', 'reliability', '可靠性',
];

const offTopicSignals = [
  'snapchat', 'apple', '苹果', '高速', 'meta 解雇', 'contractor',
  'color theory', '颜色理论', '色彩理论', 'marketing', '营销',
  'hacker news top stories', '早报', 'musk', '马斯克', '诉讼',
  'human intelligence augmentation', '人类智能增强',
];

function walk(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) out.push(...walk(p));
    else if (name === 'article.md') out.push(p);
  }
  return out;
}

function read(file) {
  return fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
}

function includesAny(text, terms) {
  const lower = text.toLowerCase();
  return terms.filter((term) => lower.includes(term.toLowerCase()));
}

function titleFrom(articleText, summaryText) {
  return (
    (articleText.match(/^#\s+(.+)$/m) || [])[1]
    || (summaryText.match(/^- Title:\s*(.+)$/m) || [])[1]
    || ''
  ).trim();
}

function sourceFrom(sourceText) {
  return {
    bestblogs: (sourceText.match(/^- BestBlogs URL:\s*(.+)$/m) || [])[1] || '',
    original: (sourceText.match(/^- Original publisher URL:\s*(.+)$/m) || [])[1] || '',
  };
}

function classify(row) {
  if (/欢迎来到 BestBlogs|登录或注册/.test(row.articleStart)) {
    return { status: '错误抓取', reason: '正文像登录/欢迎页' };
  }

  if (row.strongHits.length >= 4) return { status: '强相关', reason: '' };
  if (row.strongHits.length >= 2 && row.offTopicHits.length === 0) return { status: '相关', reason: '' };
  if (row.strongHits.length >= 2 && row.offTopicHits.length <= 1) return { status: '需人工复核', reason: `有少量偏题信号: ${row.offTopicHits.join(', ')}` };
  if (row.strongHits.length === 1 && row.broadHits.length >= 2 && row.offTopicHits.length === 0) return { status: '弱相关', reason: '只有一个强 Agent 词，但有 AI/工程宽泛相关性' };
  if (row.broadHits.length >= 3 && row.offTopicHits.length === 0) return { status: '弱相关', reason: '偏 AI/工程生态，但 Agent 直接性弱' };
  if (row.offTopicHits.length > 0) return { status: '疑似无关', reason: `偏题信号: ${row.offTopicHits.join(', ')}` };
  return { status: '疑似无关', reason: '缺少 Agent/AI 工程关键词' };
}

const rows = [];

for (const article of walk(ITEMS_ROOT)) {
  const dir = path.dirname(article);
  const id = path.basename(dir);
  const topic = path.basename(path.dirname(dir));
  const summaryPath = path.join(dir, 'summary.md');
  const sourcePath = path.join(dir, 'source.md');
  const articleText = read(article);
  const summaryText = fs.existsSync(summaryPath) ? read(summaryPath) : '';
  const sourceText = fs.existsSync(sourcePath) ? read(sourcePath) : '';
  const title = titleFrom(articleText, summaryText);
  const combined = `${title}\n${summaryText}\n${articleText.slice(0, 16000)}`;
  const row = {
    id,
    topic,
    title,
    chars: articleText.length,
    article,
    ...sourceFrom(sourceText),
    strongHits: includesAny(combined, strongTerms),
    broadHits: includesAny(combined, weakOrBroadTerms),
    offTopicHits: includesAny(combined, offTopicSignals),
    articleStart: articleText.slice(0, 1000),
  };
  Object.assign(row, classify(row));
  rows.push(row);
}

rows.sort((a, b) => a.id.localeCompare(b.id));

const counts = rows.reduce((acc, row) => {
  acc[row.status] = (acc[row.status] || 0) + 1;
  return acc;
}, {});

const lines = [
  '# Knowledge Relevance Audit',
  '',
  `Generated: ${new Date().toISOString()}`,
  '',
  'Scope: checks whether collected BestBlogs items are useful for the user\'s AI agent learning knowledge base.',
  '',
  '## Counts',
  '',
];

for (const status of ['强相关', '相关', '弱相关', '需人工复核', '疑似无关', '错误抓取']) {
  if (counts[status]) lines.push(`- ${status}: ${counts[status]}`);
}

lines.push(
  '',
  '## Review Table',
  '',
  '| ID | Status | Strong Hits | Broad Hits | Topic | Chars | Title | Reason |',
  '| --- | --- | ---: | ---: | --- | ---: | --- | --- |',
);

for (const row of rows) {
  lines.push(`| ${row.id} | ${row.status} | ${row.strongHits.length} | ${row.broadHits.length} | ${row.topic} | ${row.chars} | ${row.title.replace(/\|/g, '/')} | ${(row.reason || '').replace(/\|/g, '/')} |`);
}

lines.push('', '## Items Needing Human Review', '');
for (const row of rows.filter((r) => !['强相关', '相关'].includes(r.status))) {
  lines.push(`- ${row.id} [${row.status}] ${row.title}`);
  lines.push(`  - Reason: ${row.reason || 'n/a'}`);
  lines.push(`  - Strong hits: ${row.strongHits.join(', ') || 'none'}`);
  lines.push(`  - Broad hits: ${row.broadHits.join(', ') || 'none'}`);
  lines.push(`  - BestBlogs: ${row.bestblogs}`);
  lines.push(`  - Original: ${row.original}`);
}

fs.writeFileSync(REPORT, `${lines.join('\n')}\n`, 'utf8');

console.log(JSON.stringify({
  total: rows.length,
  counts,
  review: rows
    .filter((r) => !['强相关', '相关'].includes(r.status))
    .map((r) => ({
      id: r.id,
      status: r.status,
      strongHits: r.strongHits.length,
      broadHits: r.broadHits.length,
      title: r.title,
      reason: r.reason,
    })),
}, null, 2));
