from pathlib import Path
import re

ROOT = Path(r'D:\newwork\aiagentstudy')
old_dir = ROOT / 'knowledge' / 'items' / '02-tools-actions' / 'BB-2026-05-01-170'
new_dir = ROOT / 'knowledge' / 'items' / '02-tools-actions' / 'BB-2026-05-01-252'
index_path = ROOT / 'knowledge' / 'catalog' / 'articles-index.md'
memory_path = ROOT / 'AI_AGENT_MEMORY.md'

if not old_dir.exists():
    raise SystemExit('old dir missing')
if new_dir.exists():
    raise SystemExit('new dir already exists')

old_dir.rename(new_dir)

summary_path = new_dir / 'summary.md'
text = summary_path.read_text(encoding='utf-8-sig')
text = re.sub(r'^# BB-2026-05-01-170 Summary$', '# BB-2026-05-01-252 Summary', text, flags=re.M)
summary_path.write_text(text, encoding='utf-8')

index = index_path.read_text(encoding='utf-8-sig')
line = '| BB-2026-05-01-252 | 05-12 | Best practices for computer and browser use with Claude / Claude | BestBlogs / Claude Blog | `02-tools-actions` | Tools/Actions, Control Loop, Deliverable | Full text + source captured |'
if 'BB-2026-05-01-252' not in index:
    index = index.rstrip() + '\n' + line + '\n'
    index_path.write_text(index, encoding='utf-8')

memory = memory_path.read_text(encoding='utf-8-sig')
note = '- On 2026-05-24, repaired a historical duplicate id conflict by moving the accidentally duplicated Claude computer/browser-use article from `BB-2026-05-01-170` to `BB-2026-05-01-252`, preserving the original `BB-2026-05-01-170` for the Kimi Agent Infra article.\n'
if note not in memory:
    memory = memory.rstrip() + '\n' + note
    memory_path.write_text(memory, encoding='utf-8')

print('moved', old_dir, '->', new_dir)
print('updated summary/index/memory')
