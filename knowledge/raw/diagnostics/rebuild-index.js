const fs = require('fs');
const rows = [
 ['BB-2026-05-01-001','2026-04-27','Harness 不是目的，知识才是护城河','BestBlogs / 腾讯技术工程','`01-context-memory`','Context/State, Memory, Evaluation, Deliverable','Summary created; full export pending'],
 ['BB-2026-05-01-002','2026-04-29','Codex 与子智能体：OpenAI AI 工程平台深度解析','BestBlogs / AI Engineer','`03-control-loop`','Tools/Actions, Control Loop, Evaluation, Deliverable','Metadata summary'],
 ['BB-2026-05-01-003','2026-04-24','对罗福莉访谈：AI 范式已然巨变，Agent 范式很吃后训练','BestBlogs / 商业访谈录','`06-frontier-radar`','Model, Control Loop, Evaluation','Metadata summary'],
 ['BB-2026-05-01-004','2026-04-29','Demis Hassabis 谈 AGI 路径、架构缺口与深科技创业','BestBlogs / Y Combinator','`06-frontier-radar`','Model, Reasoning/Planning, Frontier Radar','Metadata summary'],
 ['BB-2026-05-01-005','2026-04-27','OpenAI 推出 gpt-realtime-1.5，打造语音交互应用','BestBlogs / OpenAI Developers','`06-frontier-radar`','Model, Tools/Actions, Product Workflow','Metadata summary'],
 ['BB-2026-05-01-006','2026-04-27','像带新人一样引导 Claude Code','BestBlogs / Claude Blog','`03-control-loop`','Context/State, Tools/Actions, Control Loop','Meta summary'],
 ['BB-2026-05-01-007','2026-04-30','RAG 已死？不，是 Grep 回归了！','BestBlogs / 腾讯云开发者','`01-context-memory`','Context/State, Tools/Actions, Evaluation','Meta summary'],
 ['BB-2026-05-01-008','2026-04-24','DeepSeek-V4 预览版：迈入百万上下文普惠时代','BestBlogs / DeepSeek','`06-frontier-radar`','Model, Context/State, Control Loop','Meta summary'],
 ['BB-2026-05-01-009','2026-04-26','Snapchat CEO Evan Spiegel：分发成为护城河','BestBlogs / Lenny\'s Podcast','`06-frontier-radar`','Product Workflow','Low-priority meta summary']
];
let md = '# Articles Index\n\nCompact index of collected items.\n\n| ID | Date | Title | Source | Topic | Blocks | Status |\n| --- | --- | --- | --- | --- | --- | --- |\n';
for (const r of rows) md += `| ${r.join(' | ')} |\n`;
fs.writeFileSync('knowledge/catalog/articles-index.md', md, 'utf8');
