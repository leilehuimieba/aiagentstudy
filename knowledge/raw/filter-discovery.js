const fs = require('fs');
const path = require('path');
const dir = 'knowledge/raw/discovery';
const keywords = /agent|codex|claude|openai|gpt|rag|llm|deepseek|gemini|cursor|mcp|realtime|ai engineer|anthropic|chatgpt/i;
for (const file of fs.readdirSync(dir).filter(f=>f.endsWith('.json')).sort()) {
  let text = fs.readFileSync(path.join(dir,file),'utf8').replace(/^\uFEFF/, '');
  let arr;
  try { arr = JSON.parse(text); } catch(e) { console.log('parse failed', file, e.message); continue; }
  const matches = arr.filter(s => keywords.test(s)).filter((v,i,a)=>a.indexOf(v)===i);
  console.log('\n##', file, matches.length);
  for (const m of matches.slice(0,60)) console.log(m);
}
