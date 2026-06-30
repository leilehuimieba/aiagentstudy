import json, re
from pathlib import Path
import requests

ROOT = Path(r'D:\newwork\aiagentstudy')
entries = [
  {"id":"RAW_e372ffbd","title":"Insights from the Codex Official Team: How to Maximize Codex's Potential","readUrl":"https://www.bestblogs.dev/article/e372ffbd","sourceName":"宝玉的分享","publishDateStr":"05-20"},
  {"id":"RAW_c5bb1e16","title":"When Agents Truly Enter Complex Data Analysis Scenarios: DataClawBench Uses 492 Real-World Tasks for a Process-Level Examination of Frontier Models","readUrl":"https://www.bestblogs.dev/article/c5bb1e16","sourceName":"AI前线","publishDateStr":"05-21"},
  {"id":"RAW_12cfb9bb","title":"The Next War Is Already Here. The West Isn't Ready. — Yaroslav Azhnyuk， The Fourth Law & Guest Host Noah Smith， Noahpinion","readUrl":"https://www.bestblogs.dev/article/12cfb9bb","sourceName":"Latent Space","publishDateStr":"05-18"},
  {"id":"RAW_9be68136","title":"Gemini 3.5 Flash: more expensive， but Google plan to use it for everything","readUrl":"https://www.bestblogs.dev/article/9be68136","sourceName":"Simon Willison's Weblog","publishDateStr":"05-20"},
  {"id":"RAW_d92190a7","title":"[AINews] Google I/O 2026: Gemini 3.5 Flash， Omni (NanoBanana for Video)， Spark (background agents)， and Antigravity 2.0","readUrl":"https://www.bestblogs.dev/article/d92190a7","sourceName":"Latent Space","publishDateStr":"05-20"},
  {"id":"RAW_330ed662","title":"AI Transformation Levels L1-L4 for Software Companies: From Personal Tools to Business Restructuring (with Real Case Study)","readUrl":"https://www.bestblogs.dev/article/330ed662","sourceName":"SaaS白夜行","publishDateStr":"05-19"},
  {"id":"RAW_0866439a","title":"TencentDB Agent Memory is Now Open Source Globally: Let Agents Accumulate Experience, Let Humans Focus on Creation","readUrl":"https://www.bestblogs.dev/article/0866439a","sourceName":"腾讯云开发者","publishDateStr":"05-19"},
  {"id":"RAW_82054607","title":"Maintainability sensors for coding agents","readUrl":"https://www.bestblogs.dev/article/82054607","sourceName":"Martin Fowler","publishDateStr":"05-20"},
  {"id":"RAW_04b41b70","title":"Building a Self-Evolving Company with AI","readUrl":"https://www.bestblogs.dev/article/04b41b70","sourceName":"刘小排r","publishDateStr":"05-20"},
  {"id":"RAW_d142a736","title":"How Snapchat Serves a Billion Predictions Per Second","readUrl":"https://www.bestblogs.dev/article/d142a736","sourceName":"ByteByteGo Newsletter","publishDateStr":"05-19"},
]

existing_originals = {}
existing_titles = {}
for p in (ROOT / 'knowledge' / 'items').rglob('source.md'):
    text = p.read_text(encoding='utf-8-sig', errors='ignore')
    m1 = re.search(r'^- Original publisher URL:\s*(.+?)\s*$', text, re.M)
    m2 = re.search(r'^- Title:\s*(.+?)\s*$', text, re.M)
    if m1:
        existing_originals[m1.group(1).strip()] = str(p)
    if m2:
        existing_titles.setdefault(m2.group(1).strip(), []).append(str(p))

s = requests.Session(); s.trust_env = False
headers = {'User-Agent':'Mozilla/5.0','Accept':'application/json,text/plain,*/*'}
rows=[]
for item in entries:
    slug = item['readUrl'].rsplit('/',1)[-1]
    referer = item['readUrl'].replace('https://www.bestblogs.dev/article/', 'https://www.bestblogs.dev/en/article/')
    r = s.get(f'https://www.bestblogs.dev/api/proxy/resources/{slug}/page?language=en', headers={**headers,'Referer':referer}, timeout=90)
    r.raise_for_status()
    md = r.json()['data']['metaData']
    original = md.get('url') or 'Not found'
    title = md.get('title') or item['title']
    rows.append({
        'slug': slug,
        'title': title,
        'original_url': original,
        'dup_by_original': existing_originals.get(original),
        'dup_by_title': existing_titles.get(title),
    })
print(json.dumps(rows, ensure_ascii=False, indent=2))
