"""Draft generation via the claude CLI. See backend_service_specs/build.md."""
import datetime
import glob
import subprocess
from pathlib import Path

from scout.util import PROJECT_ROOT, log_event, read_json, slugify, write_json

CANDIDATES_DIR = PROJECT_ROOT / "candidates"
DRAFTS_DIR = PROJECT_ROOT / "drafts"
FAILED_DIR = DRAFTS_DIR / "failed"
PROMPT_TEMPLATE = PROJECT_ROOT / "prompts" / "build.md"
LOGS_DIR = PROJECT_ROOT / "logs"

TIMEOUT_SECONDS = 600


def _load_all_candidates():
    candidates = []
    for path in sorted(glob.glob(str(CANDIDATES_DIR / "discovery-*.json"))):
        candidates.extend(read_json(Path(path), default=[]))
    return candidates


def _already_handled(name_slug: str) -> bool:
    return (DRAFTS_DIR / name_slug).exists() or (FAILED_DIR / name_slug).exists()


def _build_prompt(candidate: dict) -> str:
    template = PROMPT_TEMPLATE.read_text()
    return template.format(
        name=candidate.get("name", ""),
        url=candidate.get("url", ""),
        description=candidate.get("description", ""),
    )


def run(limit=None) -> dict:
    all_candidates = _load_all_candidates()
    to_process = [
        c for c in all_candidates
        if not _already_handled(slugify(c.get("name", "unnamed")))
    ]
    if limit is not None:
        to_process = to_process[:limit]

    total = len(to_process)
    drafted = 0
    failed = 0

    if total == 0:
        print("build: nothing to do (no undrafted candidates)", flush=True)
        return {"drafted": 0, "failed": 0}

    for i, candidate in enumerate(to_process, start=1):
        name_slug = slugify(candidate.get("name", "unnamed"))
        print(f"[{i}/{total}] building {name_slug} ...", flush=True)

        prompt = _build_prompt(candidate)
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        log_path = LOGS_DIR / f"build-{timestamp}-{name_slug}.log"

        try:
            result = subprocess.run(
                ["claude", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
            log_path.write_text(f"error: {exc}\n")
            fail_dir = FAILED_DIR / name_slug
            fail_dir.mkdir(parents=True, exist_ok=True)
            write_json(fail_dir / "candidate.json", candidate)
            failed += 1
            print(f"  -> failed ({exc})", flush=True)
            log_event("build", f"[{i}/{total}] {name_slug}: failed ({exc})")
            continue

        log_path.write_text(f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}\n")

        if result.returncode != 0 or not result.stdout.strip():
            fail_dir = FAILED_DIR / name_slug
            fail_dir.mkdir(parents=True, exist_ok=True)
            write_json(fail_dir / "candidate.json", candidate)
            failed += 1
            print(f"  -> failed (exit {result.returncode})", flush=True)
            log_event("build", f"[{i}/{total}] {name_slug}: failed (exit {result.returncode})")
            continue

        draft_dir = DRAFTS_DIR / name_slug
        draft_dir.mkdir(parents=True, exist_ok=True)
        (draft_dir / "SKILL.md").write_text(result.stdout)
        write_json(draft_dir / "candidate.json", candidate)
        drafted += 1
        print("  -> drafted", flush=True)
        log_event("build", f"[{i}/{total}] {name_slug}: drafted")

    return {"drafted": drafted, "failed": failed}
