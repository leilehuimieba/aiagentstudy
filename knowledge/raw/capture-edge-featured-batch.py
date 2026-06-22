import json
import re
import html
import time
from pathlib import Path
import requests
from requests.exceptions import RequestException

ROOT = Path(r'D:\newwork\aiagentstudy')
RAW_LIST = ROOT / 'knowledge' / 'raw' / 'current-edge-featured-articles.json'
INDEX = ROOT / 'knowledge' / 'catalog' / 'articles-index.md'
MEMORY = ROOT / 'AI_AGENT_MEMORY.md'
REPORT_DIR = ROOT / 'knowledge' / 'raw'

MANUAL = {
    'b71c47ef': ('02-tools-actions', 'Tools/Actions, Control Loop, Deliverable'),
    'af4d392e': ('02-tools-actions', 'Tools/Actions, Control Loop, Deliverable'),
    'fc0bb3b3': ('02-tools-actions, Control Loop, Deliverable', 'Tools/Actions, Control Loop, Deliverable'),
    'de4dffe1': ('02-tools-actions', 'Tools/Actions, Control Loop, Deliverable'),
    'd7f4c3b7': ('02-tools-actions', 'Tools/Actions, Control Loop, Deliverable'),
    '4ab3a76d': ('03-control-loop', 'Goal, Control Loop, Tools/Actions, Evaluation'),
    'ae472ac6': ('03-control-loop', 'Goal, Control Loop, Tools/Actions, Evaluation'),
    '339ffc01': ('04-evaluation-guardrails', 'Evaluation, Guardrails, Tools/Actions'),
    '8fdfe4e8': ('04-evaluation-guardrails', 'Evaluation, Guardrails, Tools/Actions'),
    '3dc786a9': ('06-frontier-radar', 'Model, Frontier Radar, Product Workflow'),
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json,text/plain,*/*',
    'Connection': 'close',
}

session = requests.Session()
session.trust_env = False


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8-sig')


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def normalize_bestblogs(url: str) -> str:
    return str(url or '').replace('https://www.bestblogs.dev/en/', 'https://www.bestblogs.dev/').split('?', 1)[0].split('#', 1)[0]


def existing_urls():
    seen = set()
    for p in (ROOT / 'knowledge' / 'items').rglob('source.md'):
        txt = p.read_text(encoding='utf-8-sig', errors='ignore')
        m = re.search(r'^- BestBlogs URL:\s*(https://www\.bestblogs\.dev/(?:en/)?(?:article|video|podcast|status|explore/topics)/\S+)\s*$', txt, re.M)
        if m:
            seen.add(normalize_bestblogs(m.group(1)))
    return seen


def next_id_base() -> int:
    nums = [int(x) for x in re.findall(r'BB-2026-05-01-(\d{3})', read_text(INDEX))]
    return (max(nums) if nums else 0) + 1


def md_cell(text: str) -> str:
    return str(text or '').replace('|', '/').replace('\r', ' ').replace('\n', ' ').strip()


def strip_html(doc: str) -> str:
    text = doc
    text = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', '\n', text)
    text = re.sub(r'(?i)</(p|div|section|article|h1|h2|h3|h4|h5|h6|li|ul|ol|blockquote|pre|table|tr)>', '\n', text)
    text = re.sub(r'(?i)<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


def fetch_json(url: str, referer: str, retries: int = 5):
    headers = dict(HEADERS)
    headers['Referer'] = referer
    last = None
    for attempt in range(1, retries + 1):
        try:
            r = session.get(url, headers=headers, timeout=90)
            r.raise_for_status()
            return r.json(), r.content
        except RequestException as e:
            last = e
            time.sleep(min(2 * attempt, 10))
    raise last


def append_memory(lines):
    old = read_text(MEMORY).rstrip() + '\n'
    marker = '\n## Recent Updates\n'
    if marker not in old:
        old += marker
    insert = ''.join(f'- {line}\n' for line in lines)
    write_text(MEMORY, old.rstrip() + '\n' + insert)


obj = json.loads(read_text(RAW_LIST))
entries = obj['body']['data']['dataList']
seen = existing_urls()
start = next_id_base()
results = []
errors = []
index_append = []
memory_notes = []

for item in entries:
    read_url = item['readUrl']
    norm = normalize_bestblogs(read_url)
    if norm in seen:
        continue
    slug = norm.rsplit('/', 1)[-1]
    topic, blocks = MANUAL.get(slug, ('06-frontier-radar', 'Model, Frontier Radar, Product Workflow'))
    if topic == '02-tools-actions, Control Loop, Deliverable':
        topic = '02-tools-actions'
    bbid = f"BB-2026-05-01-{start + len(results):03d}"
    referer = read_url.replace('https://www.bestblogs.dev/article/', 'https://www.bestblogs.dev/en/article/')

    try:
        page_json, page_bytes = fetch_json(f'https://www.bestblogs.dev/api/proxy/resources/{slug}/page?language=en', referer)
        time.sleep(1)
        content_json, content_bytes = fetch_json(f'https://www.bestblogs.dev/api/proxy/resources/{slug}/content?language=en', referer)
    except Exception as e:
        errors.append({'planned_id': bbid, 'slug': slug, 'readUrl': read_url, 'error': str(e)})
        continue

    md = page_json['data']['metaData']
    content_data = content_json['data']['contentData']
    plain = strip_html(content_data['displayDocument'])

    source = f"BestBlogs / {md.get('sourceName') or 'Unknown source'}"
    title = md.get('title') or item.get('title') or slug
    date = md.get('publishDateStr') or md.get('publishDateTimeStr', '')[:10]
    published_full = md.get('publishDateTimeStr') or ''
    tags = md.get('tags') or []
    original_url = md.get('url') or 'Not found'

    item_dir = ROOT / 'knowledge' / 'items' / topic / bbid
    raw_dir = item_dir / 'raw'
    raw_dir.mkdir(parents=True, exist_ok=True)

    (raw_dir / 'page.json').write_bytes(page_bytes)
    (raw_dir / 'content.json').write_bytes(content_bytes)
    write_text(raw_dir / 'discovery.json', json.dumps(item, ensure_ascii=False, indent=2) + '\n')

    article_md = (
        f"# {title}\n\n"
        f"- BestBlogs URL: {read_url}\n"
        f"- Original publisher URL: {original_url}\n"
        f"- Source: {source}\n"
        f"- Publish time: {published_full}\n"
        f"- Capture route: article discovered from logged-in Edge/OpenCLI browser session; page/content captured from BestBlogs resource APIs\n"
        f"- Extracted chars: {len(plain)}\n\n"
        f"---\n\n{plain}"
    )
    write_text(item_dir / 'article.md', article_md)

    source_md = (
        f"# Source Evidence\n\n"
        f"- Title: {title}\n"
        f"- BestBlogs URL: {read_url}\n"
        f"- Original publisher URL: {original_url}\n"
        f"- BestBlogs source label: {md.get('sourceName') or ''}\n"
        f"- Publish time: {published_full}\n"
        f"- Language: {md.get('languageDesc') or md.get('language') or ''}\n"
        f"- Score: {md.get('score')}\n"
        f"- Word count: {md.get('wordCount')}\n\n"
        f"## Evidence Notes\n\n"
        f"- Discovery source: logged-in Edge/OpenCLI session list endpoint (`/api/proxy/resources?page=1&pageSize=10&timeFilter=1w&language=all&sortType=default&type=ARTICLE&qualifiedFilter=true&uiLang=en`).\n"
        f"- Detail source: BestBlogs resource page/content endpoints for slug `{slug}`.\n"
    )
    write_text(item_dir / 'source.md', source_md)

    summary_md = (
        f"# {bbid} Summary\n\n"
        f"## Article\n\n"
        f"- Title: {title}\n"
        f"- Source: {source}\n"
        f"- URL: {read_url}\n"
        f"- Date: {date}\n"
        f"- Topic: `{topic}`\n"
        f"- Tags: {', '.join(tags) if tags else ''}\n\n"
        f"## Model Mapping\n\n"
        f"- Blocks: {blocks}\n"
        f"- Layer: captured frontier material, pending deep reading\n\n"
        f"## Core Takeaway\n\n"
        f"{md.get('summary') or md.get('oneSentenceSummary') or 'Full text captured for later selective reading and synthesis.'}\n\n"
        f"## Reusable Principle\n\n"
        f"{md.get('featuredReason') or 'Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.'}\n"
    )
    write_text(item_dir / 'summary.md', summary_md)

    status = 'Full text + source captured' if len(plain) > 800 else 'Short page captured'
    index_append.append(f"| {bbid} | {md_cell(date)} | {md_cell(title)} | {md_cell(source)} | `{topic}` | {md_cell(blocks)} | {status} |")
    results.append((bbid, slug, title, topic, len(plain)))
    memory_notes.append(f"On 2026-05-24, captured {bbid}: {title} ({topic}, slug `{slug}`) using the logged-in Edge/OpenCLI browser session for discovery, with full text, source evidence, and raw page/content JSON saved.")
    seen.add(norm)
    time.sleep(1)

if index_append:
    write_text(INDEX, read_text(INDEX).rstrip() + '\n' + '\n'.join(index_append) + '\n')
    append_memory(memory_notes)

report = {
    'captured_count': len(results),
    'start_id': results[0][0] if results else None,
    'end_id': results[-1][0] if results else None,
    'items': results,
    'errors': errors,
}
write_text(REPORT_DIR / f"edge-featured-batch-{start:03d}-{start + max(len(results)-1,0):03d}.json", json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
