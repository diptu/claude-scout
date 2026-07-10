"""LLM Council gate: a second, independent check that runs after committee.py
scores a draft "hired" on quality. Mirrors the five-advisor + chairman
methodology in .claude/skills/llm-council/SKILL.md, scoped to one question:
is this candidate actually worth adding given what's already in library/, or
is it redundant? committee.py calls evaluate() directly instead of promoting
a "hired" draft on its own — this and committee.py are the two sanctioned
LLM-as-judge gates in this project; see CLAUDE.md.

Council-approved ("add") drafts are left in drafts/ for a human to make the
final promote call via `make review` — this gate narrows what reaches a
human, it does not replace them. Council-rejected ("skip", i.e. judged
redundant) drafts are trashed automatically, same as a committee reject.

If the chairman can't reach a usable synthesis (e.g. too many advisor calls
failed), evaluate() fails open to "add" rather than silently trashing a
draft on partial data — mirrors committee.py's no-quorum-leaves-for-review
stance.
"""
import json
import re
import subprocess  # nosec B404

from scout.core.config import PROJECT_ROOT, load_config

ADVISOR_PROMPT_FILE = PROJECT_ROOT / "prompts" / "council_advisor.md"
CHAIRMAN_PROMPT_FILE = PROJECT_ROOT / "prompts" / "council_chairman.md"

DEFAULT_ADVISORS = [
    {"name": "The Contrarian",
     "lens": "Search for fatal flaws and overlooked risks in adding this — argue for "
             "*not* adding it if a good case exists."},
    {"name": "The First Principles Thinker",
     "lens": "Question whether this is really a new capability or just a rephrasing of "
             "something already in the library."},
    {"name": "The Expansionist",
     "lens": "Look for upside — does this cover real ground the existing library doesn't, "
             "even if it overlaps partially?"},
    {"name": "The Outsider",
     "lens": "Judge with no attachment to either the candidate or the existing library — "
             "is this obviously redundant bookkeeping, or a genuine gap being filled?"},
    {"name": "The Executor",
     "lens": "Focus on practical outcome — if added, would anyone actually reach for this "
             "over what's already there?"},
]
TIMEOUT_SECONDS = 120

JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _council_config() -> list:
    cfg = load_config().get("council", {})
    return cfg.get("advisors", DEFAULT_ADVISORS)


def _run_claude(prompt: str):
    return subprocess.run(  # nosec B603 B607
        ["claude", "-p", prompt],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=TIMEOUT_SECONDS,
        check=False,
    )


def _parse_verdict(raw: str, key: str, valid: tuple):
    """Extract the JSON object an advisor/chairman returned. None on any
    failure (no JSON, wrong shape, invalid verdict value) so callers can
    treat it as a non-response rather than crash the whole run."""
    match = JSON_OBJECT_RE.search(raw or "")
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    verdict = data.get(key)
    if verdict not in valid:
        return None
    return {"verdict": verdict, "reason": str(data.get("reason", ""))[:200]}


def _cast_advisor_opinions(skill_md: str, library_names: str, advisors: list,
                            log_lines: list) -> list:
    template = ADVISOR_PROMPT_FILE.read_text(encoding="utf-8")
    opinions = []
    for advisor in advisors:
        prompt = template.format(
            advisor_name=advisor["name"],
            advisor_lens=advisor["lens"],
            library_names=library_names,
            skill_md_content=skill_md,
        )
        try:
            result = _run_claude(prompt)
        except subprocess.TimeoutExpired:
            log_lines.append(f"{advisor['name']}: TIMEOUT")
            continue
        raw = result.stdout or ""
        log_lines.append(f"{advisor['name']}: {raw}")
        if result.returncode != 0:
            continue
        parsed = _parse_verdict(raw, "verdict", ("add", "skip"))
        if parsed is not None:
            opinions.append({"advisor": advisor["name"], **parsed})
    return opinions


def _chairman_synthesize(skill_md: str, opinions: list, log_lines: list):
    if not opinions:
        return None
    template = CHAIRMAN_PROMPT_FILE.read_text(encoding="utf-8")
    opinions_text = "\n".join(
        f"- {o['advisor']}: {o['verdict']} — {o['reason']}" for o in opinions
    )
    prompt = template.format(advisor_opinions=opinions_text, skill_md_content=skill_md)
    try:
        result = _run_claude(prompt)
    except subprocess.TimeoutExpired:
        log_lines.append("Chairman: TIMEOUT")
        return None
    raw = result.stdout or ""
    log_lines.append(f"Chairman: {raw}")
    if result.returncode != 0:
        return None
    return _parse_verdict(raw, "decision", ("add", "skip"))


def evaluate(skill_md: str, library_names: str) -> dict:
    """Runs the five-advisor + chairman deliberation for one candidate.
    Returns {"decision": "add"|"skip", "reason": str, "advisors": [...],
    "log_lines": [...]}."""
    advisors = _council_config()
    log_lines: list[str] = []
    opinions = _cast_advisor_opinions(skill_md, library_names, advisors, log_lines)
    chairman = _chairman_synthesize(skill_md, opinions, log_lines)
    if chairman is None:
        return {
            "decision": "add",
            "reason": "chairman synthesis unavailable (too few advisor responses), "
                      "deferring to human review instead of auto-deciding",
            "advisors": opinions,
            "log_lines": log_lines,
        }
    return {
        "decision": chairman["verdict"],
        "reason": chairman["reason"],
        "advisors": opinions,
        "log_lines": log_lines,
    }
