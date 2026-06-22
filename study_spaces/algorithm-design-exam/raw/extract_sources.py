from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
SPACE = ROOT / 'study_spaces' / 'algorithm-design-exam'
RAW = SPACE / 'raw'
MANIFEST = RAW / 'source-manifest.json'
OUT = RAW / 'extracted'
SOFFICE = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding='utf-8'))


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)


def clean_text(text: str) -> str:
    text = text.replace('\r', '\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    parts = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            txt = page.extract_text() or ''
        except Exception as exc:
            txt = f'[PDF page {i} extract error: {exc}]\n'
        parts.append(f'\n\n===== PAGE {i} =====\n\n{txt}')
    return clean_text(''.join(parts))


def convert_doc_to_docx_and_txt(src: Path, out_dir: Path) -> tuple[Path | None, Path | None, str]:
    ensure_dir(out_dir)
    log_parts = []

    docx_result = run([
        str(SOFFICE), '--headless', '--convert-to', 'docx', '--outdir', str(out_dir), str(src)
    ])
    log_parts.append('DOCX convert stdout:\n' + (docx_result.stdout or ''))
    log_parts.append('DOCX convert stderr:\n' + (docx_result.stderr or ''))

    txt_result = run([
        str(SOFFICE), '--headless', '--convert-to', 'txt:Text', '--outdir', str(out_dir), str(src)
    ])
    log_parts.append('TXT convert stdout:\n' + (txt_result.stdout or ''))
    log_parts.append('TXT convert stderr:\n' + (txt_result.stderr or ''))

    docx_path = out_dir / (src.stem + '.docx')
    txt_path = out_dir / (src.stem + '.txt')
    if not docx_path.exists():
        docx_path = None
    if not txt_path.exists():
        txt_path = None

    return docx_path, txt_path, '\n\n'.join(log_parts)


def write_text(path: Path, text: str) -> None:
    path.write_text(clean_text(text), encoding='utf-8')


def main() -> None:
    ensure_dir(OUT)
    manifest = read_manifest()
    report = {
        'generated_from': str(MANIFEST),
        'outputs': [],
    }

    for item in manifest['files']:
        src = Path(item['path'])
        item_dir = OUT / item['id']
        ensure_dir(item_dir)

        meta = {
            'id': item['id'],
            'name': item['name'],
            'path': item['path'],
            'ext': item['ext'],
            'size_bytes': item['size_bytes'],
            'suggested_role': item['suggested_role'],
            'review_phase': item['review_phase'],
            'status': 'pending',
        }

        shutil.copy2(src, item_dir / src.name)

        extract_log = []
        text_output = item_dir / 'content.txt'
        if item['ext'].lower() == '.pdf':
            text = extract_pdf_text(src)
            write_text(text_output, text)
            meta['status'] = 'extracted'
            meta['text_path'] = str(text_output)
            meta['chars'] = len(text)
        elif item['ext'].lower() == '.doc':
            docx_path, txt_path, log = convert_doc_to_docx_and_txt(src, item_dir)
            extract_log.append(log)
            if txt_path and txt_path.exists():
                raw_text = txt_path.read_text(encoding='utf-8', errors='ignore')
                write_text(text_output, raw_text)
                meta['status'] = 'extracted'
                meta['text_path'] = str(text_output)
                meta['chars'] = len(raw_text)
            else:
                meta['status'] = 'txt-convert-failed'
            if docx_path:
                meta['docx_path'] = str(docx_path)
        else:
            meta['status'] = 'unsupported-extension'

        (item_dir / 'extract.log').write_text('\n\n'.join(extract_log) if extract_log else 'No conversion log.\n', encoding='utf-8')
        (item_dir / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        report['outputs'].append(meta)

    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'items': len(report['outputs']),
        'extracted': sum(1 for x in report['outputs'] if x['status'] == 'extracted'),
        'report': str(OUT / 'report.json'),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
