const fs=require('fs');
const path=require('path');
const indexed = new Set((fs.readFileSync('knowledge/catalog/articles-index.md','utf8').match(/BB-\d{4}-\d{2}-\d{2}-\d{3}/g)||[]));
const files = fs.readdirSync('knowledge/raw/discovery').filter(f=>f.endsWith('.json'));
const urlMap = new Map();
for(const f of files){
 let arr; try{arr=JSON.parse(fs.readFileSync(path.join('knowledge/raw/discovery',f),'utf8').replace(/^\uFEFF/,''));}catch{continue;}
 for(const s of arr){
  const [hrefRaw, textRaw=''] = String(s).split(' || ');
  const href = hrefRaw.trim(); const text=textRaw.trim().replace(/\s+/g,' ');
  if(!href || !text) continue;
  if(!/(article|video|podcast|status|newsletter|topics)\//.test(href)) continue;
  const clean = href.split('?')[0];
  if(!urlMap.has(clean)) urlMap.set(clean,{href:clean,text,from:new Set()});
  urlMap.get(clean).from.add(f);
 }
}
const keywords = /Agent|agent|Codex|Claude|OpenAI|GPT|RAG|MCP|Harness|Karpathy|Software|智能体|模型|编程|上下文|记忆|工具|基建|工程|Code|Cursor|OpenClaw|Hermes|Managed|Cloudflare|LangChain|MiniMax|Kimi|GLM|Gemini|Qwen/i;
const candidates=[...urlMap.values()].filter(x=>keywords.test(x.text)).map(x=>({href:x.href,text:x.text,from:[...x.from]}));
console.log(JSON.stringify(candidates, null, 2));
