"""Small file/name helpers shared across scout/*.py (3+ call sites, past the
project's own de-duplication threshold — see TODO.md)."""
import datetime
import json
import re
from pathlib import Path

# src/scout/util.py -> parent=src/scout, parent.parent=src, parent.parent.parent=repo root.
# Centralized here (rather than recomputed per module) since every scout/*.py
# module needs it and the src/ layout means it's no longer a trivial one-liner.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    return slug or "unnamed"


def read_json(path: Path, default=None):
    if not path.exists():
        return default
    with path.open() as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(data, f, indent=2)


def log_event(stage: str, message: str) -> None:
    """Append one timestamped line to logs/<stage>.log — a per-stage run
    summary, distinct from build.py/eval.py's separate per-candidate
    transcript logs (which capture full claude stdout/stderr, not summaries)."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (LOGS_DIR / f"{stage}.log").open("a") as f:
        f.write(f"{timestamp} {message}\n")
