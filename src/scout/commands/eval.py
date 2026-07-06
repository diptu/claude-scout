"""Eval gate: "does it run," never quality. See backend_service_specs/eval.md.

Before running the fixed battery (prompts/eval_tests.md), each draft gets a
verification call: claude is asked whether the standard prompts apply to this
particular skill, and if not, to design one short tailored test instead. The
LLM designs tests; it never grades answers — pass/fail is still exit codes
and timeouts only (TODO.md principle 6)."""
import datetime
import re
import shutil
import subprocess  # nosec B404

from scout.core.config import PROJECT_ROOT
from scout.core.logger import log_event

DRAFTS_DIR = PROJECT_ROOT / "drafts"
FAILED_EVAL_DIR = DRAFTS_DIR / "failed-reason-eval"
EVAL_PROMPTS_FILE = PROJECT_ROOT / "prompts" / "eval_tests.md"
LOGS_DIR = PROJECT_ROOT / "logs"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
TIMEOUT_SECONDS = 120
SKIP_DIR_NAMES = {"failed", "failed-reason-eval"}

APPLICABLE_KEYWORD = "APPLICABLE"


def _has_valid_frontmatter(content: str) -> bool:
    match = FRONTMATTER_RE.match(content)
    if not match:
        return False
    fm = match.group(1)
    return "name:" in fm and "description:" in fm


def _extract_prompts():
    text = EVAL_PROMPTS_FILE.read_text(encoding="utf-8")
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


def _run_claude(prompt: str):
    return subprocess.run(  # nosec B603 B607
        ["claude", "-p", prompt],
        capture_output=True,
        # claude emits UTF-8; without this, Windows decodes with the locale
        # codepage and stdout becomes None on the first non-cp1252 byte.
        encoding="utf-8",
        errors="replace",
        timeout=TIMEOUT_SECONDS,
        check=False,
    )


def _verify_or_design_tests(content: str, prompts: list, log_lines: list):
    """Ask claude whether the standard battery applies to this skill. Returns
    (prompts_to_run, battery_label); any verification hiccup falls back to
    the standard battery rather than blocking the eval."""
    listed = "\n".join(f"- {p}" for p in prompts)
    verify_prompt = (
        "You are vetting smoke tests for a Claude Code skill.\n"
        "Here are the standard test prompts:\n"
        f"{listed}\n\n"
        f"If these prompts make sense as smoke tests for the skill below, reply "
        f"with ONLY the word {APPLICABLE_KEYWORD}. If they do not apply to it, "
        "reply with ONLY one short replacement test prompt (a single imperative "
        "sentence) tailored to this skill. No other text.\n\n---\n"
        f"{content}"
    )
    try:
        result = _run_claude(verify_prompt)
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        log_lines.append(f"verify: {exc} — falling back to standard battery")
        return prompts, "standard"

    answer = (result.stdout or "").strip()
    log_lines.append(f"verify answer:\n{answer}")
    if result.returncode != 0 or not answer:
        return prompts, "standard"
    if answer.upper().startswith(APPLICABLE_KEYWORD):
        return prompts, "standard"
    custom = answer.splitlines()[0].strip().strip('"')
    return [custom], "custom"


def _run_test_prompts(content: str, prompts: list, log_lines: list) -> bool:
    for p_i, prompt in enumerate(prompts, start=1):
        print(f"  prompt {p_i}/{len(prompts)} ...", flush=True)
        full_prompt = f"{prompt}\n\n---\n{content}"
        try:
            result = _run_claude(full_prompt)
        except subprocess.TimeoutExpired:
            log_lines.append("TIMEOUT")
            return False
        log_lines.append(result.stdout or "")
        if result.returncode != 0:
            return False
    return True


def run() -> dict:
    passed = 0
    failed = 0
    report: list[dict] = []
    prompts = _extract_prompts()
    claude_available = _claude_available()

    drafts = _draft_dirs_to_evaluate()
    total = len(drafts)
    if total == 0:
        print("eval: nothing to do (no unevaluated drafts)", flush=True)
        return {"passed": 0, "failed": 0, "report": []}

    for i, draft_dir in enumerate(drafts, start=1):
        print(f"[{i}/{total}] evaluating {draft_dir.name} ...", flush=True)
        content = (draft_dir / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        ok = _has_valid_frontmatter(content)
        battery = "frontmatter-only"
        tests_run = 0

        if not ok:
            battery = "-"
        elif claude_available:
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            LOGS_DIR.mkdir(parents=True, exist_ok=True)
            log_lines: list[str] = []
            draft_prompts, battery = _verify_or_design_tests(content, prompts, log_lines)
            ok = _run_test_prompts(content, draft_prompts, log_lines)
            tests_run = len(draft_prompts)
            log_path = LOGS_DIR / f"eval-{timestamp}-{draft_dir.name}.log"
            log_path.write_text("\n---\n".join(log_lines), encoding="utf-8")
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

        report.append({
            "name": draft_dir.name,
            "battery": battery,
            "tests": tests_run,
            "result": "passed" if ok else "failed",
        })

    return {"passed": passed, "failed": failed, "report": report}
