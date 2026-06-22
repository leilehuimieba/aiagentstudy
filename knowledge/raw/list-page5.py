import json, pathlib
p = pathlib.Path(r'knowledge/raw/current-opencli-latest-page5-20260601.json')
data = json.loads(p.read_text(encoding='utf-8-sig'))
for i, item in enumerate(data['data']['dataList'], 1):
    slug = item['readUrl'].rsplit('/', 1)[-1]
    print(f"{i:02d}\t{slug}\t{item['title']}")
