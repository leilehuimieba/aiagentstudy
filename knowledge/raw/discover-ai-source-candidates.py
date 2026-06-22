import argparse
import json
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "knowledge" / "sources" / "source-registry.json"
OUT_DIR = ROOT / "knowledge" / "raw" / "source-candidates"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


DEFAULT_HEADERS = {
    "User-Agent": "aiagentstudy-source-discovery/1.0",
    "Accept": "application/atom+xml,application/rss+xml,application/xml,text/xml,text/html,*/*",
}


def fetch_text(url, timeout=60):
    session = requests.Session()
    session.trust_env = False
    response = session.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def text_of(element, names):
    for name in names:
        if name.startswith("atom:"):
            found = element.find(f"{{http://www.w3.org/2005/Atom}}{name.split(':', 1)[1]}")
        else:
            found = element.find(name)
        if found is not None and found.text:
            return found.text.strip()
    return ""


def parse_atom_entries(xml_text):
    root = ET.fromstring(xml_text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = []
    for entry in root.findall("atom:entry", ns):
        links = []
        for link in entry.findall("atom:link", ns):
            href = link.attrib.get("href")
            if href:
                links.append({"href": href, "rel": link.attrib.get("rel", ""), "type": link.attrib.get("type", "")})
        entries.append(
            {
                "title": text_of(entry, ["atom:title"]),
                "summary": text_of(entry, ["atom:summary"]),
                "published": text_of(entry, ["atom:published"]),
                "updated": text_of(entry, ["atom:updated"]),
                "id": text_of(entry, ["atom:id"]),
                "authors": [text_of(author, ["atom:name"]) for author in entry.findall("atom:author", ns)],
                "links": links,
            }
        )
    return entries


def parse_rss_entries(xml_text):
    root = ET.fromstring(xml_text)
    entries = []
    channel = root.find("channel")
    if channel is None:
        return entries
    for item in channel.findall("item"):
        entries.append(
            {
                "title": text_of(item, ["title"]),
                "summary": text_of(item, ["description"]),
                "published": text_of(item, ["pubDate"]),
                "updated": "",
                "id": text_of(item, ["guid"]),
                "authors": [],
                "links": [{"href": text_of(item, ["link"]), "rel": "alternate", "type": "text/html"}],
            }
        )
    return entries


def discover_arxiv(query, max_results):
    encoded = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": "0",
            "max_results": str(max_results),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    url = f"https://export.arxiv.org/api/query?{encoded}"
    xml_text = fetch_text(url, timeout=90)
    return {
        "source_id": "arxiv",
        "url": url,
        "query": query,
        "entries": parse_atom_entries(xml_text),
    }


def discover_rss(source_id, url, limit):
    xml_text = fetch_text(url, timeout=90)
    if "<rss" in xml_text[:200].lower():
        entries = parse_rss_entries(xml_text)
    else:
        entries = parse_atom_entries(xml_text)
    return {
        "source_id": source_id,
        "url": url,
        "query": "",
        "entries": entries[:limit],
    }


def main():
    parser = argparse.ArgumentParser(description="Discover source candidates without creating durable knowledge items.")
    parser.add_argument("--arxiv-query", default='all:"AI agent" OR all:"large language model" OR all:"tool use"')
    parser.add_argument("--max-results", type=int, default=20)
    parser.add_argument(
        "--rss",
        nargs="*",
        default=[],
        help="RSS source IDs from source-registry.json, e.g. huggingface-blog google-deepmind",
    )
    args = parser.parse_args()

    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    by_id = {}
    for group in registry["groups"]:
        for source in group["sources"]:
            by_id[source["id"]] = source

    discoveries = [discover_arxiv(args.arxiv_query, args.max_results)]
    time.sleep(1)

    for source_id in args.rss:
        source = by_id.get(source_id)
        if not source or not source.get("rss"):
            discoveries.append({"source_id": source_id, "error": "missing rss URL in registry"})
            continue
        try:
            discoveries.append(discover_rss(source_id, source["rss"], args.max_results))
        except Exception as exc:
            discoveries.append({"source_id": source_id, "url": source.get("rss"), "error": str(exc)})
        time.sleep(1)

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "candidate-discovery",
        "discoveries": discoveries,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"source-candidates-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out_path), "sources": len(discoveries)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
