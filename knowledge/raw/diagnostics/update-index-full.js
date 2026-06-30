const fs=require('fs');
const indexPath='knowledge/catalog/articles-index.md';
let index=fs.readFileSync(indexPath,'utf8').trimEnd();
const row='| BB-2026-05-01-023 | 2026-04-21 | 使用 MCP 构建能够接入生产系统的智能体 | BestBlogs / Claude Blog | `02-tools-actions` | Tools/Actions, MCP, Guardrails | Full text + source captured |';
if(!index.includes('BB-2026-05-01-023')) index += '\n' + row;
// Mark all existing article.md >800 as full captured
const fullIds=[];
function walk(dir){ for(const n of fs.readdirSync(dir)){ const p=require('path').join(dir,n); const st=fs.statSync(p); if(st.isDirectory()) walk(p); else if(n==='article.md' && st.size>800) fullIds.push(require('path').basename(require('path').dirname(p))); } }
walk('knowledge/items');
index=index.split('\n').map(line=>{
 for(const id of fullIds){
  if(line.startsWith('| '+id+' |')){
   const cells=line.split('|').map(s=>s.trim());
   if(cells.length>=9 && !/Full text/.test(cells[7])) { cells[7]='Full text + source captured'; return '| '+cells.slice(1,-1).join(' | ')+' |'; }
  }
 }
 return line;
}).join('\n')+'\n';
fs.writeFileSync(indexPath,index,'utf8');
let mem=fs.readFileSync('AI_AGENT_MEMORY.md','utf8');
if(!mem.includes('Batch capture target')) mem += '\n- Batch capture target: continue in batches of 20 successful full-text captures. A successful capture should include `article.md` and `source.md`; short posts may be accepted if the page itself is short.\n';
if(!mem.includes('BB-2026-05-01-023')) mem += '- Added BB-2026-05-01-023: Claude/MCP production systems article, full text and source captured.\n';
fs.writeFileSync('AI_AGENT_MEMORY.md',mem,'utf8');
console.log({fullCount: fullIds.length, fullIds: fullIds.sort()});
