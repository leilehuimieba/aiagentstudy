const fs = require('fs');
const path = require('path');
function readJson(p){ return JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,'')); }
function writeSource(dir, opts){
  const lines = ['# Source Evidence','',`- Title: ${opts.title || ''}`,`- BestBlogs URL: ${opts.bestblogsUrl || ''}`];
  if (opts.type === 'topic') {
    lines.push('- Item type: BestBlogs topic page / curated guide');
    lines.push('- Original publisher URL: Not applicable; this is a BestBlogs topic page.');
  } else {
    lines.push(`- Original publisher URL: ${opts.originalUrl || 'Not found on page during capture.'}`);
    if (opts.originalText) lines.push(`- Original link text: ${opts.originalText}`);
  }
  lines.push('','## Evidence Links Captured','');
  for (const l of (opts.links || []).slice(0,40)) lines.push(`- ${l.text || l.title || l.href}: ${l.href}`);
  fs.writeFileSync(path.join(dir,'source.md'), lines.join('\n')+'\n','utf8');
}
// normal article source links
for (const [dir, rawPath] of [
 ['knowledge/items/01-context-memory/BB-2026-05-01-007','knowledge/items/01-context-memory/BB-2026-05-01-007/raw/source-links.json'],
 ['knowledge/items/03-control-loop/BB-2026-05-01-010','knowledge/items/03-control-loop/BB-2026-05-01-010/raw/source-links.json']
]){
 const data = readJson(rawPath);
 const orig = (data.originalLinks || [])[0];
 writeSource(dir,{title:data.title,bestblogsUrl:data.bestblogsUrl,originalUrl:orig&&orig.href,originalText:orig&&(orig.text||orig.title),links:data.externalLinks||[]});
}
// 016 from inspect because source-links captured a transient 504
{
 const dir='knowledge/items/01-context-memory/BB-2026-05-01-016';
 const data=readJson('knowledge/raw/inspect/BB-2026-05-01-016.json');
 const links=data.links||[];
 const orig=links.find(x=>x.text && x.text.includes('查看原文'));
 const external=links.filter(x=>x.href && !x.href.includes('bestblogs.dev'));
 writeSource(dir,{title:data.title,bestblogsUrl:data.url,originalUrl:orig&&orig.href,originalText:orig&&(orig.text||orig.title),links:external});
}
// topic pages
for (const [dir, rawPath] of [
 ['knowledge/items/01-context-memory/BB-2026-05-01-020','knowledge/items/01-context-memory/BB-2026-05-01-020/raw/source-links.json'],
 ['knowledge/items/03-control-loop/BB-2026-05-01-022','knowledge/items/03-control-loop/BB-2026-05-01-022/raw/source-links.json']
]){
 const data=readJson(rawPath);
 writeSource(dir,{type:'topic',title:data.title,bestblogsUrl:data.bestblogsUrl,links:data.externalLinks||[]});
}
// update index statuses
const indexPath='knowledge/catalog/articles-index.md';
let index=fs.readFileSync(indexPath,'utf8');
const fullIds=['BB-2026-05-01-007','BB-2026-05-01-010','BB-2026-05-01-016','BB-2026-05-01-020','BB-2026-05-01-022'];
index=index.split('\n').map(line=>{
 for(const id of fullIds){
  if(line.startsWith('| '+id+' |')){
    const cells=line.split('|').map(s=>s.trim());
    if(cells.length>=9){ cells[7]='Full text + source captured'; return '| '+cells.slice(1,-1).join(' | ')+' |'; }
  }
 }
 return line;
}).join('\n');
fs.writeFileSync(indexPath,index,'utf8');
