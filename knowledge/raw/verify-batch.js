const fs=require('fs'), path=require('path');
const articles=[], sources=[];
function walk(d){for(const n of fs.readdirSync(d)){const p=path.join(d,n); const st=fs.statSync(p); if(st.isDirectory()) walk(p); else if(n==='article.md') articles.push([path.basename(path.dirname(p)),st.size]); else if(n==='source.md') sources.push([path.basename(path.dirname(p)),st.size]);}}
walk('knowledge/items');
articles.sort((a,b)=>a[0].localeCompare(b[0]));
console.log('articles_gt_800=' + articles.filter(x=>x[1]>800).length);
console.log('sources=' + sources.length);
for(const a of articles) console.log(a[0]+' '+a[1]);
