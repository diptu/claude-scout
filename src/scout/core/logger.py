"""Per-stage run-summary logging (print() stays the debugging tool — TODO.md)."""
import datetime

from scout.core.config import PROJECT_ROOT

LOGS_DIR = PROJECT_ROOT / "logs"


def log_event(stage: str, message: str) -> None:
    """Append one timestamped line to logs/<stage>.log — a per-stage run
    summary, distinct from build.py/eval.py's separate per-candidate
    transcript logs (which capture full claude stdout/stderr, not summaries)."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (LOGS_DIR / f"{stage}.log").open("a") as f:
        f.write(f"{timestamp} {message}\n")
