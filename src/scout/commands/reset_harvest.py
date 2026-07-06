"""Reset harvest state: clear discovery files and the seen-URL dedup log.

Harvest is append-only (see harvest_github.py/harvest_reddit.py) — updating
defaults/config.yml only affects future queries, it never re-validates or
prunes candidates already sitting in candidates/discovery-*.json. This is
the manual reset for that: wipe discovery files + seen.txt so the next
`make harvest` repopulates from scratch under the current config. Anything
already in drafts/, library/, or trash/ is untouched.
"""
import glob
from pathlib import Path

from scout.core.config import PROJECT_ROOT

CANDIDATES_DIR = PROJECT_ROOT / "candidates"
SEEN_FILE = CANDIDATES_DIR / "seen.txt"


def _discovery_files() -> list:
    return [Path(p) for p in sorted(glob.glob(str(CANDIDATES_DIR / "discovery-*.json")))]


def run(confirm=input) -> dict:
    files = _discovery_files()
    seen_exists = SEEN_FILE.exists()

    if not files and not seen_exists:
        print("reset-harvest: nothing to reset (no discovery files or seen.txt)", flush=True)
        return {"discovery_files_removed": 0, "seen_removed": False}

    print("reset-harvest: this will permanently delete:")
    for f in files:
        print(f"  - {f}")
    if seen_exists:
        print(f"  - {SEEN_FILE}")
    print("Any candidate not yet built is lost. drafts/, library/, trash/ are untouched.")

    if confirm("Proceed? [y/N] ").strip().lower() != "y":
        print("reset-harvest: aborted", flush=True)
        return {"discovery_files_removed": 0, "seen_removed": False}

    for f in files:
        f.unlink()
    if seen_exists:
        SEEN_FILE.unlink()

    print(f"reset-harvest: removed {len(files)} discovery file(s)"
          f"{' and seen.txt' if seen_exists else ''}", flush=True)
    return {"discovery_files_removed": len(files), "seen_removed": seen_exists}
