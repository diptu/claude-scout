"""Hiring-committee gate: automatic reject, but hired drafts now pass through
a second LLM-as-judge gate (council.py) before anything is promoted.

Each voter in defaults/config.yml's `committee.voters` (fixed exec personas —
CEO, CTO, Solution Architect, Security Lead, QA Lead) scores a draft 1-5 on
usefulness/uniqueness/quality/safety via one `claude -p` call each (see
prompts/committee.md). The overall average across all successful voters and
dimensions decides the quality bar: below committee.passing_score, the draft
moves straight to trash/ — no human in the loop. >= committee.passing_score
("hired") no longer auto-promotes to library/ on its own: it's handed to
council.evaluate(), an independent LLM Council redundancy check against the
existing library/ catalog (mirrors .claude/skills/llm-council). Council
"skip" (judged redundant) trashes the draft automatically, same as a
committee reject. Council "add" leaves the draft in drafts/ untouched for a
human to make the final promote call via `make review` — committee+council
narrow what reaches a human, they don't replace them.

Below committee.min_voters (too many voter calls failed), the draft is left
untouched in drafts/ for `make review` instead of being decided on partial
data. Same for a name collision with an existing library/<name>/ entry —
skipped with zero claude calls rather than risk silently overwriting
hand-curated tags/content (a real incident during development: a stray
leftover draft sharing a name with an already-promoted skill got
auto-promoted over it before this guard existed).

Still an LLM-as-judge gate, not a smoke test — unlike eval.py, this one
scores quality on purpose. See CLAUDE.md for why that's now in scope."""
import datetime
import json
import re
import shutil
import subprocess  # nosec B404

from scout.commands import council
from scout.core.config import PROJECT_ROOT, load_config
from scout.core.logger import log_event
from scout.core.util import write_json

DRAFTS_DIR = PROJECT_ROOT / "drafts"
LIBRARY_DIR = PROJECT_ROOT / "library"
TRASH_DIR = PROJECT_ROOT / "trash"
COMMITTEE_PROMPT_FILE = PROJECT_ROOT / "prompts" / "committee.md"
LOGS_DIR = PROJECT_ROOT / "logs"
SKIP_DIR_NAMES = {"failed", "failed-reason-eval"}

DIMENSIONS = ("usefulness", "uniqueness", "quality", "safety")
DEFAULT_PASSING_SCORE = 3.5
DEFAULT_MIN_VOTERS = 3
DEFAULT_VOTERS = [
    {"name": "CEO",
     "focus": "Strategic value and ROI of adding and maintaining this skill."},
    {"name": "CTO",
     "focus": "Technical correctness and long-term maintainability of the instructions."},
    {"name": "Solution Architect",
     "focus": "Uniqueness versus the existing library catalog; overlap/redundancy with "
              "what's already there."},
    {"name": "Security Lead",
     "focus": "Safety — free of destructive actions, prompt-injection risk, or unsafe "
              "credential handling."},
    {"name": "QA Lead",
     "focus": "Clarity and testability of the steps — would a reviewer know if it worked?"},
]
TIMEOUT_SECONDS = 120

JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _committee_config() -> tuple[float, int, list]:
    cfg = load_config().get("committee", {})
    passing_score = cfg.get("passing_score", DEFAULT_PASSING_SCORE)
    min_voters = cfg.get("min_voters", DEFAULT_MIN_VOTERS)
    voters = cfg.get("voters", DEFAULT_VOTERS)
    return passing_score, min_voters, voters


def _passed_drafts():
    if not DRAFTS_DIR.exists():
        return []
    result = []
    for entry in DRAFTS_DIR.iterdir():
        if not entry.is_dir() or entry.name in SKIP_DIR_NAMES:
            continue
        status_file = entry / ".eval_status"
        if status_file.exists() and status_file.read_text().strip() == "passed":
            result.append(entry)
    return result


def _library_names() -> str:
    if not LIBRARY_DIR.exists():
        return "(none yet)"
    names = sorted(e.name for e in LIBRARY_DIR.iterdir() if e.is_dir())
    return ", ".join(names) if names else "(none yet)"


def _run_claude(prompt: str):
    return subprocess.run(  # nosec B603 B607
        ["claude", "-p", prompt],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=TIMEOUT_SECONDS,
        check=False,
    )


def _parse_vote(raw: str):
    """Extract the JSON object a voter returned. Returns None on any failure
    (missing dimension, non-numeric score, no JSON at all) so callers can
    treat this voter as a non-vote rather than crash the whole run."""
    match = JSON_OBJECT_RE.search(raw or "")
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    try:
        scores = {dim: float(data[dim]) for dim in DIMENSIONS}
    except (KeyError, TypeError, ValueError):
        return None
    if any(not 1 <= s <= 5 for s in scores.values()):
        return None
    return {"scores": scores, "reason": str(data.get("reason", ""))[:200]}


def _cast_votes(skill_md: str, voters: list, log_lines: list,
                 exclude_name: str | None = None) -> list:
    template = COMMITTEE_PROMPT_FILE.read_text(encoding="utf-8")
    library_names = _library_names()
    if exclude_name:
        # Backfilling a skill that's already in library/ would otherwise list
        # it among itself for the uniqueness comparison — nonsensical for the
        # Solution Architect persona's vote. Drop it from the string voters see.
        remaining = [n for n in library_names.split(", ") if n and n != exclude_name]
        library_names = ", ".join(remaining) if remaining else "(none yet)"
    votes = []
    for voter in voters:
        prompt = template.format(
            voter_name=voter["name"],
            voter_focus=voter["focus"],
            library_names=library_names,
            skill_md_content=skill_md,
        )
        try:
            result = _run_claude(prompt)
        except subprocess.TimeoutExpired:
            log_lines.append(f"{voter['name']}: TIMEOUT")
            continue
        raw = result.stdout or ""
        log_lines.append(f"{voter['name']}: {raw}")
        if result.returncode != 0:
            continue
        vote = _parse_vote(raw)
        if vote is not None:
            votes.append({"voter": voter["name"], **vote})
    return votes


def _overall_score(votes: list) -> float:
    all_scores = [s for vote in votes for s in vote["scores"].values()]
    return sum(all_scores) / len(all_scores)


def _reject(draft_dir, committee_verdict: dict, council_verdict: dict | None = None) -> None:
    dest = TRASH_DIR / draft_dir.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.move(str(draft_dir), str(dest))
    write_json(dest / "committee_verdict.json", committee_verdict)
    if council_verdict is not None:
        write_json(dest / "council_verdict.json", council_verdict)


def _hold_for_review(draft_dir, committee_verdict: dict, council_verdict: dict) -> None:
    """Council approved it, but committee.py never auto-promotes a hired
    draft on its own — leave it in place so `make review` picks it up for
    the final human call, same as a no-quorum or name-collision draft."""
    write_json(draft_dir / "committee_verdict.json", committee_verdict)
    write_json(draft_dir / "council_verdict.json", council_verdict)


def _run_council_gate(draft_dir, skill_md: str, committee_verdict: dict, timestamp: str) -> str:
    """Runs the council check for a committee-hired draft and applies its
    verdict — trash if judged redundant, hold in place if worth adding.
    Returns the resulting report decision string."""
    overall = committee_verdict["overall_score"]
    council_result = council.evaluate(skill_md, _library_names())
    (LOGS_DIR / f"council-{timestamp}-{draft_dir.name}.log").write_text(
        "\n---\n".join(council_result["log_lines"]), encoding="utf-8")
    council_verdict = {
        "decision": council_result["decision"],
        "reason": council_result["reason"],
        "advisors": council_result["advisors"],
    }

    if council_result["decision"] == "skip":
        _reject(draft_dir, committee_verdict, council_verdict)
        print(f"  -> hired (avg {overall}/5) but council judged it redundant, trashed",
              flush=True)
        return "duplicate"

    _hold_for_review(draft_dir, committee_verdict, council_verdict)
    print(f"  -> hired (avg {overall}/5) and council-approved, left for `make review`",
          flush=True)
    return "pending-review"


def _process_draft(i: int, total: int, draft_dir, committee_config: tuple) -> dict:
    """Decides (and, past the quorum check, acts on) the fate of one draft.
    Returns a report row: {"name", "votes", "score", "decision"} where
    decision is one of name-collision / already-decided / no-quorum /
    rejected / duplicate / pending-review."""
    passing_score, min_voters, voters = committee_config
    print(f"[{i}/{total}] committee voting on {draft_dir.name} ...", flush=True)

    if (LIBRARY_DIR / draft_dir.name).exists():
        # A same-named entry is already curated in library/ (e.g. a stray
        # leftover draft) — never auto-overwrite hand-curated tags/content.
        # Leave the draft alone for a human to reconcile via `make review`
        # or by deleting the redundant draft directly.
        print(f"  -> name collision with existing library/{draft_dir.name}, "
              "left for manual reconciliation", flush=True)
        return {"name": draft_dir.name, "votes": 0, "score": None, "decision": "name-collision"}

    if (draft_dir / "committee_verdict.json").exists():
        # Already hired + council-approved on a previous run and left here
        # for `make review` — don't re-spend voter/advisor calls re-deciding
        # something already decided.
        print("  -> already decided, pending `make review`", flush=True)
        return {"name": draft_dir.name, "votes": 0, "score": None, "decision": "already-decided"}

    skill_md = (draft_dir / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    log_lines: list[str] = []
    votes = _cast_votes(skill_md, voters, log_lines)

    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (LOGS_DIR / f"committee-{timestamp}-{draft_dir.name}.log").write_text(
        "\n---\n".join(log_lines), encoding="utf-8")

    if len(votes) < min_voters:
        print(f"  -> no quorum ({len(votes)}/{len(voters)} voted), left for `make review`",
              flush=True)
        return {"name": draft_dir.name, "votes": len(votes), "score": None,
                "decision": "no-quorum"}

    overall = round(_overall_score(votes), 2)
    committee_decision = "hired" if overall >= passing_score else "rejected"
    committee_verdict = {
        "overall_score": overall,
        "passing_score": passing_score,
        "decision": committee_decision,
        "votes": votes,
    }

    if committee_decision == "rejected":
        _reject(draft_dir, committee_verdict)
        print(f"  -> rejected (avg {overall}/5, {len(votes)}/{len(voters)} voted)", flush=True)
        return {"name": draft_dir.name, "votes": len(votes), "score": overall,
                "decision": "rejected"}

    # Hired by committee on quality — now check with the council whether
    # it's actually worth adding given what's already in library/.
    decision = _run_council_gate(draft_dir, skill_md, committee_verdict, timestamp)
    return {"name": draft_dir.name, "votes": len(votes), "score": overall, "decision": decision}


_BUCKET_BY_DECISION = {
    "name-collision": "collisions",
    "already-decided": "already_decided",
    "no-quorum": "no_quorum",
    "rejected": "rejected",
    "duplicate": "duplicate",
    "pending-review": "pending_review",
}


def run() -> dict:
    passing_score, min_voters, voters = _committee_config()
    drafts = _passed_drafts()
    total = len(drafts)
    report: list[dict] = []
    counts = dict.fromkeys(set(_BUCKET_BY_DECISION.values()), 0)

    if total == 0:
        print("committee: nothing to do (no eval-passed drafts)", flush=True)
        return {**counts, "report": []}

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    committee_config = (passing_score, min_voters, voters)
    for i, draft_dir in enumerate(drafts, start=1):
        row = _process_draft(i, total, draft_dir, committee_config)
        counts[_BUCKET_BY_DECISION[row["decision"]]] += 1
        if row["score"] is not None:
            log_event("committee", f"[{i}/{total}] {row['name']}: {row['decision']} "
                                    f"(avg {row['score']})")
        report.append(row)

    return {**counts, "report": report}
