const fs = require('fs');
const entries = [
  {
    id:'BB-2026-05-01-010', dir:'knowledge/items/03-control-loop/BB-2026-05-01-010',
    row:['BB-2026-05-01-010','2026-04-30','Codex CLI 0.128.0 新增 /goal 命令','BestBlogs / Simon Willison','`03-control-loop`','Goal, Control Loop, Evaluation, Deliverable','Meta summary'],
    md:`# BB-2026-05-01-010 Summary\n\n## Article\n\n- Title: Codex CLI 0.128.0 新增 /goal 命令\n- Source: BestBlogs / Simon Willison\n- URL: https://www.bestblogs.dev/article/5de75aba\n- Date: 2026-04-30\n- Topic: \`03-control-loop\`\n- Tags: Codex CLI, OpenAI, AI 编码智能体, Ralph 循环, 自主编码\n\n## Model Mapping\n\n- Blocks: Goal, Control Loop, Evaluation/Guardrails, Deliverable\n- Layer: engineering, architecture, frontier radar\n\n## Core Takeaway\n\nThe new \`/goal\` command matters because it makes the agent loop explicit: define a target, let the coding agent iterate autonomously, and stop when the goal is reached or the token budget is exhausted.\n\n## Reusable Principle\n\nA strong agent interface should expose goal-directed loops, budget limits, and stopping conditions. Autonomy without an explicit goal and budget is hard to evaluate.\n\n## Follow-Up Questions\n\n- How does \`/goal\` decide success?\n- What evidence does it produce when stopping?\n- How should this connect to tests, CI, or PR review?\n`
  },
  {
    id:'BB-2026-05-01-011', dir:'knowledge/items/04-evaluation-guardrails/BB-2026-05-01-011',
    row:['BB-2026-05-01-011','2026-04-30','OpenAI GPT-5.5 网络能力评估','BestBlogs / Simon Willison','`04-evaluation-guardrails`','Evaluation, Guardrails, Model','Meta summary'],
    md:`# BB-2026-05-01-011 Summary\n\n## Article\n\n- Title: 我们对 OpenAI GPT-5.5 网络能力的评估\n- Source: BestBlogs / Simon Willison\n- URL: https://www.bestblogs.dev/article/29a3b9f4\n- Date: 2026-04-30\n- Topic: \`04-evaluation-guardrails\`\n- Tags: GPT-5.5, AI 安全, 网络安全, 漏洞发现, AI 安全研究所\n\n## Model Mapping\n\n- Blocks: Model, Evaluation/Guardrails\n- Layer: evaluation, safety, frontier radar\n\n## Core Takeaway\n\nThis item is relevant as a model-capability and safety evaluation case. It highlights that advanced models may have meaningful cyber capabilities, so agent systems need capability-aware permissions, logging, and evaluation.\n\n## Reusable Principle\n\nAgent reliability evaluation is incomplete without misuse and high-risk capability evaluation. Stronger models require stronger guardrails, not only better benchmarks.\n\n## Follow-Up Questions\n\n- What tasks were used to evaluate cyber capability?\n- How should tool permissions change for higher-capability models?\n- What should an agent log when operating in security-sensitive environments?\n`
  },
  {
    id:'BB-2026-05-01-012', dir:'knowledge/items/04-evaluation-guardrails/BB-2026-05-01-012',
    row:['BB-2026-05-01-012','2026-04-30','被色彩理论难住的 GenAI','BestBlogs / Theresa-Marie Rhyne','`04-evaluation-guardrails`','Evaluation, Tools/Actions, Context/State','Meta summary'],
    md:`# BB-2026-05-01-012 Summary\n\n## Article\n\n- Title: 被色彩理论难住的 GenAI\n- Source: BestBlogs / Theresa-Marie Rhyne\n- URL: https://www.bestblogs.dev/article/c517725e\n- Date: 2026-04-30\n- Topic: \`04-evaluation-guardrails\`\n- Tags: Perplexity AI, 色彩理论, 可访问性, 数据可视化, 感知均匀颜色空间\n\n## Model Mapping\n\n- Blocks: Evaluation/Guardrails, Tools/Actions, Context/State\n- Layer: evaluation, applied AI\n\n## Core Takeaway\n\nThis is a useful small case for evaluating AI systems on specialized domain constraints. A model may produce plausible answers while failing expert requirements such as accessibility or perceptual uniformity.\n\n## Reusable Principle\n\nFor domain-specific tasks, evaluation must include domain-specific acceptance criteria. Plausible output is not the same as correct output.\n\n## Agent Learning Use\n\nUse this as an example when discussing eval design: define constraints, test outputs against them, and avoid trusting general reasoning without verification.\n`
  },
  {
    id:'BB-2026-05-01-013', dir:'knowledge/items/06-frontier-radar/BB-2026-05-01-013',
    row:['BB-2026-05-01-013','2026-04-30','马斯克在 OpenAI 庭审中的 7 大失误','BestBlogs / Ashley Belanger','`06-frontier-radar`','Ecosystem, Governance','Low-priority meta summary'],
    md:`# BB-2026-05-01-013 Summary\n\n## Article\n\n- Title: 马斯克在 OpenAI 庭审中的 7 大失误\n- Source: BestBlogs / Ashley Belanger\n- URL: https://www.bestblogs.dev/article/af3386fe\n- Date: 2026-04-30\n- Topic: \`06-frontier-radar\`\n- Tags: 埃隆·马斯克, OpenAI, 庭审, 山姆·奥特曼, 诉讼\n\n## Model Mapping\n\n- Blocks: Ecosystem, Governance\n- Layer: frontier radar, industry context\n- Priority: low for core agent learning\n\n## Core Takeaway\n\nThis is ecosystem context about OpenAI governance and litigation. Keep it as background; it is not directly about agent architecture or engineering.\n`
  },
  {
    id:'BB-2026-05-01-014', dir:'knowledge/items/06-frontier-radar/BB-2026-05-01-014',
    row:['BB-2026-05-01-014','2026-04-30','HSEE 资助轮与人类智能增强项目','BestBlogs / LessWrong','`06-frontier-radar`','Frontier Radar, Human Intelligence Augmentation','Low-priority meta summary'],
    md:`# BB-2026-05-01-014 Summary\n\n## Article\n\n- Title: SFF 的 HSEE 资助轮；我希望看到的人类智能增强项目\n- Source: BestBlogs / LessWrong\n- URL: https://www.bestblogs.dev/article/62051a71\n- Date: 2026-04-30\n- Topic: \`06-frontier-radar\`\n- Tags: 人类智能增强, 生殖遗传学, 资助, 认知增强, LessWrong\n\n## Model Mapping\n\n- Blocks: Frontier Radar, Human Intelligence Augmentation\n- Layer: frontier radar, adjacent field\n- Priority: low for core agent learning\n\n## Core Takeaway\n\nThis is adjacent to AI-agent learning. It belongs in frontier radar as context on human intelligence augmentation, not as an agent engineering article.\n`
  }
];
for (const e of entries) {
  fs.mkdirSync(e.dir, {recursive:true});
  fs.writeFileSync(`${e.dir}/summary.md`, e.md, 'utf8');
}
const indexPath = 'knowledge/catalog/articles-index.md';
let index = fs.readFileSync(indexPath, 'utf8').replace(/^\uFEFF/, '').trimEnd();
for (const e of entries) {
  if (!index.includes(e.id)) index += `\n| ${e.row.join(' | ')} |`;
}
index += '\n';
fs.writeFileSync(indexPath, index, 'utf8');
