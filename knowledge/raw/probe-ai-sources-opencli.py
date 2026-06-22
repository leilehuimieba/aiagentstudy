import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "knowledge" / "sources" / "source-registry.json"
OUT_DIR = ROOT / "knowledge" / "sources" / "opencli-probes"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def extract_json_object(output: str):
    decoder = json.JSONDecoder()
    for i, ch in enumerate(output):
        if ch in "[{":
            try:
                obj, _ = decoder.raw_decode(output[i:])
                return obj
            except json.JSONDecodeError:
                continue
    return None


def run_opencli(args, timeout=90):
    opencli_bin = shutil.which("opencli") or shutil.which("opencli.cmd") or "opencli.cmd"
    proc = subprocess.run(
        [opencli_bin, *args],
        cwd=str(ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def load_registry():
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def flatten_sources(registry):
    out = {}
    for group in registry["groups"]:
        for source in group["sources"]:
            row = dict(source)
            row["group_id"] = group["id"]
            row["group_name"] = group["name"]
            out[row["id"]] = row
    return out


def probe_source(profile, source):
    opened = run_opencli(["browser", profile, "tab", "new", source["url"]], timeout=90)
    page_info = extract_json_object(opened["stdout"]) if opened["returncode"] == 0 else None

    result = {
        "source_id": source["id"],
        "name": source["name"],
        "group_id": source["group_id"],
        "requested_url": source["url"],
        "capture_route": source.get("capture_route"),
        "browser_needed": source.get("browser_needed"),
        "open": {
            "returncode": opened["returncode"],
            "stderr": opened["stderr"].strip(),
            "page": page_info,
        },
    }

    if opened["returncode"] != 0:
        result["status"] = "open_failed"
        return result

    if page_info and page_info.get("page"):
        selected = run_opencli(["browser", profile, "tab", "select", page_info["page"]], timeout=30)
        result["select"] = {
            "returncode": selected["returncode"],
            "stderr": selected["stderr"].strip(),
            "page": extract_json_object(selected["stdout"]),
        }

    eval_js = (
        "(()=>{"
        "const text=(document.body&&document.body.innerText||'').replace(/\\s+/g,' ').trim();"
        "return {"
        "url:location.href,"
        "title:document.title,"
        "readyState:document.readyState,"
        "textLength:text.length,"
        "sample:text.slice(0,1200),"
        "links:[...document.querySelectorAll('a[href]')].slice(0,20).map(a=>({text:(a.innerText||a.ariaLabel||'').trim().slice(0,80),href:a.href}))"
        "};"
        "})()"
    )
    tab_id = page_info.get("page") if page_info else None
    eval_args = ["browser", profile, "eval", eval_js]
    if tab_id:
        eval_args.extend(["--tab", tab_id])

    evaluated = {"returncode": 1, "stdout": "", "stderr": "not run"}
    page_state = None
    for attempt in range(3):
        if attempt:
            time.sleep(2)
        evaluated = run_opencli(eval_args, timeout=90)
        page_state = extract_json_object(evaluated["stdout"]) if evaluated["returncode"] == 0 else None
        if page_state and page_state.get("url") != "about:blank" and page_state.get("textLength", 0) > 0:
            break
    result["eval"] = {
        "returncode": evaluated["returncode"],
        "stderr": evaluated["stderr"].strip(),
        "page_state": page_state,
    }

    if evaluated["returncode"] != 0:
        result["status"] = "eval_failed"
    elif page_state and page_state.get("textLength", 0) > 500:
        result["status"] = "browser_readable"
    elif page_state:
        result["status"] = "browser_opened_low_text"
    else:
        result["status"] = "eval_unparsed"
    return result


def main():
    parser = argparse.ArgumentParser(description="Probe AI source websites through OpenCLI Browser Bridge.")
    parser.add_argument("--profile", default="qmvqcrb8")
    parser.add_argument("--ids", nargs="*", help="Source IDs to probe. Defaults to a small representative set.")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()

    registry = load_registry()
    sources = flatten_sources(registry)
    selected_ids = args.ids or [
        "arxiv",
        "huggingface-papers",
        "openai-news",
        "anthropic-news",
        "google-deepmind",
        "langchain-blog",
        "vllm",
        "jiqizhixin",
    ]
    selected = [sources[source_id] for source_id in selected_ids[: args.limit] if source_id in sources]

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "profile": args.profile,
        "source_count": len(selected),
        "results": [probe_source(args.profile, source) for source in selected],
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"source-probe-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({**report, "output": str(out_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
