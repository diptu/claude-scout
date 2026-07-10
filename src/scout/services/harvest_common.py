"""Shared flat-file plumbing for discovery sources: candidates/seen.txt,
candidates/discovery-<date>.json, and the library/ URL cross-check. Each
source's own run() still owns all its fetch/parse/threshold logic — this is
only the identical bookkeeping tail every source used to duplicate. Per
CLAUDE.md principle 2 ("duplicate at two, de-duplicate at three"): with five
harvesters now sharing this exact code, the extraction earns its keep. Paths
are passed in rather than read from module globals so each source keeps its
own CANDIDATES_DIR/SEEN_FILE/LIBRARY_DIR constants (and stays independently
monkeypatchable in tests)."""
import datetime
from pathlib import Path

from scout.core.util import read_json, write_json


def load_seen(seen_file: Path) -> set:
    if not seen_file.exists():
        return set()
    return set(seen_file.read_text().splitlines())


def library_urls(library_dir: Path) -> set:
    """URLs already promoted to library/ — checked in addition to seen.txt
    so a reset-harvest (which wipes seen.txt) doesn't re-add skills that
    are already curated."""
    if not library_dir.exists():
        return set()
    urls = set()
    for entry in library_dir.iterdir():
        url = read_json(entry / "meta.json", default={}).get("source_url")
        if url:
            urls.add(url)
    return urls


def append_seen(seen_file: Path, urls) -> None:
    seen_file.parent.mkdir(parents=True, exist_ok=True)
    with seen_file.open("a") as f:
        for url in urls:
            f.write(url + "\n")


def write_candidates(candidates_dir: Path, seen_file: Path,
                      new_candidates: list, new_urls: list) -> None:
    if not new_candidates:
        return
    today_file = candidates_dir / f"discovery-{datetime.date.today().isoformat()}.json"
    existing = read_json(today_file, default=[])
    write_json(today_file, existing + new_candidates)
    append_seen(seen_file, new_urls)
