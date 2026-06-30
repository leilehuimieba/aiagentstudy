const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const BESTBLOGS = 'https://www.bestblogs.dev';

const items = [
  { id: 'BB-2026-05-01-039', href: '/zh/newsletter/issue92', topic: '06-frontier-radar' },
  { id: 'BB-2026-05-01-040', href: '/zh/newsletter/issue91', topic: '06-frontier-radar' },
  { id: 'BB-2026-05-01-041', href: '/zh/newsletter/issue90', topic: '03-control-loop' },
  { id: 'BB-2026-05-01-042', href: '/zh/newsletter/issue89', topic: '06-frontier-radar' },
  { id: 'BB-2026-05-01-043', href: '/zh/newsletter/issue85', topic: '06-frontier-radar' },
  { id: 'BB-2026-05-01-044', href: '/zh/newsletter/issue84', topic: '03-control-loop' },
  { id: 'BB-2026-05-01-045', href: '/zh/newsletter/issue83', topic: '03-control-loop' },
];

function readUtf8(file) {
  return fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
}

function writeUtf8(file, text) {
  fs.writeFileSync(file, text, 'utf8');
}

function titleFromText(text) {
  const first = text.split(/\r?\n/).map((x) => x.trim()).find(Boolean) || '';
  return first.replace(/^最新一期\s*/, '').slice(0, 120);
}

function updateIndexStatus(id, status) {
  const indexPath = path.join(ROOT, 'knowledge', 'catalog', 'articles-index.md');
  const lines = readUtf8(indexPath).split(/\r?\n/);
  const next = lines.map((line) => {
    if (!line.startsWith(`| ${id} |`)) return line;
    const cells = line.split('|');
    if (cells.length >= 9) cells[7] = ` ${status} `;
    return cells.join('|');
  }).join('\n');
  writeUtf8(indexPath, next.endsWith('\n') ? next : `${next}\n`);
}

const candidates = JSON.parse(readUtf8(path.join(ROOT, 'knowledge', 'raw', 'candidates-2.json')));
const report = [];

for (const item of items) {
  const candidate = candidates.find((x) => x.href === item.href);
  if (!candidate || !candidate.text || candidate.text.length < 800) {
    report.push({ id: item.id, href: item.href, ok: false, reason: 'candidate long text not found' });
    continue;
  }

  const dir = path.join(ROOT, 'knowledge', 'items', item.topic, item.id);
  const rawDir = path.join(dir, 'raw');
  fs.mkdirSync(rawDir, { recursive: true });

  const domPath = path.join(rawDir, 'dom-full.json');
  const dom = fs.existsSync(domPath) ? JSON.parse(readUtf8(domPath)) : {};
  const title = (dom.title || titleFromText(candidate.text)).replace(/\s*\|\s*BestBlogs\.dev\s*$/i, '').trim();
  const url = `${BESTBLOGS}${item.href}`;
  const original = (dom.links || []).find((l) => /查看原文|原文|Original|Source/i.test(l.text || l.title || ''))
    || (dom.links || []).find((l) => l.href && !l.href.includes('bestblogs.dev'));

  writeUtf8(path.join(rawDir, 'discovery-fulltext.json'), `${JSON.stringify(candidate, null, 2)}\n`);

  const article = [
    `# ${title || titleFromText(candidate.text)}`,
    '',
    `- BestBlogs URL: ${url}`,
    '- Extraction: BestBlogs detail-page DOM plus long newsletter text preserved from discovery index',
    `- Extracted chars: ${candidate.text.length}`,
    original ? `- Original publisher URL: ${original.href}` : '- Original publisher URL: Not found on page during capture.',
    '',
    '---',
    '',
    candidate.text,
    '',
  ].join('\n');
  writeUtf8(path.join(dir, 'article.md'), article);

  const sourcePath = path.join(dir, 'source.md');
  let source = fs.existsSync(sourcePath) ? readUtf8(sourcePath).trimEnd() : '# Source Evidence\n';
  if (!source.includes('discovery-fulltext.json')) {
    source += [
      '',
      '## Full-Text Recovery Note',
      '',
      '- The newsletter detail page exposed only short DOM text during capture.',
      '- Long newsletter text was recovered from `knowledge/raw/candidates-2.json` and saved as `raw/discovery-fulltext.json`.',
      `- Recovered chars: ${candidate.text.length}`,
      '',
    ].join('\n');
  }
  writeUtf8(sourcePath, source.endsWith('\n') ? source : `${source}\n`);

  const summaryPath = path.join(dir, 'summary.md');
  let summary = fs.existsSync(summaryPath) ? readUtf8(summaryPath) : '';
  summary = summary.replace('pending deep reading', 'full newsletter text captured; pending deep reading');
  writeUtf8(summaryPath, summary);

  updateIndexStatus(item.id, 'Full text + source captured');
  report.push({ id: item.id, href: item.href, ok: true, chars: candidate.text.length });
}

writeUtf8(path.join(ROOT, 'knowledge', 'raw', 'augment-newsletters-report.json'), `${JSON.stringify({ generatedAt: new Date().toISOString(), report }, null, 2)}\n`);
console.log(JSON.stringify(report, null, 2));
