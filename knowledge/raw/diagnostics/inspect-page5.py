import json, pathlib
p = pathlib.Path(r'knowledge/raw/current-opencli-latest-page5-20260601.json')
data = json.loads(p.read_text(encoding='utf-8-sig'))['data']['dataList']
for i, item in enumerate(data, 1):
    slug = item['readUrl'].rsplit('/', 1)[-1]
    print('='*80)
    print(f"{i:02d} {slug}")
    print('title:', item['title'])
    print('source:', item.get('sourceName'))
    print('date:', item.get('publishDateTimeStr'))
    print('summary:', (item.get('oneSentenceSummary') or item.get('summary') or '').replace('\n', ' '))
