"""Eval gate: "does it run," never quality. See backend_service_specs/eval.md."""
import datetime
import re
import shutil
import subprocess

from scout.util import PROJECT_ROOT, log_event

DRAFTS_DIR = PROJECT_ROOT / "drafts"
FAILED_EVAL_DIR = DRAFTS_DIR / "failed-reason-eval"
EVAL_PROMPTS_FILE = PROJECT_ROOT / "prompts" / "eval_tests.md"
LOGS_DIR = PROJECT_ROOT / "logs"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
TIMEOUT_SECONDS = 120
SKIP_DIR_NAMES = {"failed", "failed-reason-eval"}


def _has_valid_frontmatter(content: str) -> bool:
    match = FRONTMATTER_RE.match(content)
    if not match:
        return False
    fm = match.group(1)
    return "name:" in fm and "description:" in fm


def _extract_prompts():
    text = EVAL_PROMPTS_FILE.read_text()
    return re.findall(r'"([^"]+)"', text)


def _claude_available() -> bool:
    return shutil.which("claude") is not None


def _draft_dirs_to_evaluate():
    if not DRAFTS_DIR.exists():
        return []
    result = []
    for entry in DRAFTS_DIR.iterdir():
        if not entry.is_dir() or entry.name in SKIP_DIR_NAMES:
            continue
        if (entry / "SKILL.md").exists() and not (entry / ".eval_status").exists():
            result.append(entry)
    return result


def run() -> dict:
    passed = 0
    failed = 0
    prompts = _extract_prompts()
    claude_available = _claude_available()

    drafts = _draft_dirs_to_evaluate()
    total = len(drafts)
    if total == 0:
        print("eval: nothing to do (no unevaluated drafts)", flush=True)
        return {"passed": 0, "failed": 0}

    for i, draft_dir in enumerate(drafts, start=1):
        print(f"[{i}/{total}] evaluating {draft_dir.name} ...", flush=True)
        content = (draft_dir / "SKILL.md").read_text()
        ok = _has_valid_frontmatter(content)

        if ok and claude_available:
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            LOGS_DIR.mkdir(parents=True, exist_ok=True)
            log_path = LOGS_DIR / f"eval-{timestamp}-{draft_dir.name}.log"
            log_lines = []
            for p_i, prompt in enumerate(prompts, start=1):
                print(f"  prompt {p_i}/{len(prompts)} ...", flush=True)
                full_prompt = f"{prompt}\n\n---\n{content}"
                try:
                    result = subprocess.run(
                        ["claude", "-p", full_prompt],
                        capture_output=True,
                        text=True,
                        timeout=TIMEOUT_SECONDS,
                    )
                except subprocess.TimeoutExpired:
                    ok = False
                    log_lines.append("TIMEOUT")
                    break
                log_lines.append(result.stdout)
                if result.returncode != 0:
                    ok = False
                    break
            log_path.write_text("\n---\n".join(log_lines))
        # if claude is unavailable, `ok` already reflects the frontmatter-only degrade path

        if ok:
            (draft_dir / ".eval_status").write_text("passed\n")
            passed += 1
            print("  -> passed", flush=True)
            log_event("eval", f"[{i}/{total}] {draft_dir.name}: passed")
        else:
            (draft_dir / ".eval_status").write_text("failed\n")
            FAILED_EVAL_DIR.mkdir(parents=True, exist_ok=True)
            target = FAILED_EVAL_DIR / draft_dir.name
            if target.exists():
                shutil.rmtree(target)
            shutil.move(str(draft_dir), str(target))
            failed += 1
            print("  -> failed", flush=True)
            log_event("eval", f"[{i}/{total}] {draft_dir.name}: failed")

    return {"passed": passed, "failed": failed}
