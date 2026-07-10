"""Insights: aggregate the committee_verdict.json / council_verdict.json
files that committee.py and council.py already write to disk (in drafts/,
trash/, and any backfilled library/ entries) into one printed report — zero
new `claude` calls, just reading files that already exist.

Exists to answer two questions raised by the committee+council gates
themselves: which voters run hot or cold relative to the panel, and whether
committee's uniqueness dimension and council's later add/skip redundancy
call actually diverge or are scoring the same thing twice (see the
council_overlap section below)."""
from scout.core.config import PROJECT_ROOT
from scout.core.util import read_json

DRAFTS_DIR = PROJECT_ROOT / "drafts"
LIBRARY_DIR = PROJECT_ROOT / "library"
TRASH_DIR = PROJECT_ROOT / "trash"
SKIP_DIR_NAMES = {"failed", "failed-reason-eval"}

DIMENSIONS = ("usefulness", "uniqueness", "quality", "safety")


_COUNCIL_DECISION_TO_BUCKET = {"skip": "duplicate", "add": "pending-review"}


def _bucket(committee_verdict: dict, council_verdict: dict | None) -> str:
    decision = committee_verdict.get("decision")
    if decision in ("rejected", "backfilled"):
        return str(decision)
    if decision != "hired":
        return "unknown"
    if council_verdict is None:
        return "hired-no-council"
    council_decision = council_verdict.get("decision")
    if not isinstance(council_decision, str):
        return "hired-unknown-council"
    return _COUNCIL_DECISION_TO_BUCKET.get(council_decision, "hired-unknown-council")


def _iter_verdicts():
    """Every drafts/, trash/, library/ entry carrying a committee_verdict.json,
    paired with its council_verdict.json when one exists (only committee-hired
    drafts ever get a council call)."""
    for base in (DRAFTS_DIR, TRASH_DIR, LIBRARY_DIR):
        if not base.exists():
            continue
        for entry in sorted(base.iterdir()):
            if not entry.is_dir() or entry.name in SKIP_DIR_NAMES:
                continue
            committee_verdict = read_json(entry / "committee_verdict.json", default=None)
            if committee_verdict is None:
                continue
            council_verdict = read_json(entry / "council_verdict.json", default=None)
            yield committee_verdict, council_verdict


def _vote_average(scores: dict) -> float | None:
    values = [scores[d] for d in DIMENSIONS if d in scores]
    return sum(values) / len(values) if values else None


def _finalize_average(total: float, count: int) -> float | None:
    return round(total / count, 2) if count else None


def run() -> dict:
    counts: dict[str, int] = {}
    voter_totals: dict[str, list] = {}
    dim_totals_by_decision: dict[str, dict] = {}
    uniqueness_by_council_decision: dict[str, list] = {"add": [], "skip": []}

    for committee_verdict, council_verdict in _iter_verdicts():
        bucket = _bucket(committee_verdict, council_verdict)
        counts[bucket] = counts.get(bucket, 0) + 1

        decision = committee_verdict.get("decision", "unknown")
        dims = dim_totals_by_decision.setdefault(decision, {d: [0.0, 0] for d in DIMENSIONS})
        votes = committee_verdict.get("votes", [])
        for vote in votes:
            scores = vote.get("scores", {})
            for dim in DIMENSIONS:
                if dim in scores:
                    dims[dim][0] += scores[dim]
                    dims[dim][1] += 1
            avg = _vote_average(scores)
            if avg is not None:
                totals = voter_totals.setdefault(vote.get("voter", "?"), [0.0, 0])
                totals[0] += avg
                totals[1] += 1

        council_decision = (council_verdict or {}).get("decision")
        if council_decision in uniqueness_by_council_decision:
            uniqueness_scores = [v["scores"]["uniqueness"] for v in votes
                                  if "uniqueness" in v.get("scores", {})]
            if uniqueness_scores:
                uniqueness_by_council_decision[council_decision].append(
                    sum(uniqueness_scores) / len(uniqueness_scores))

    voters = [
        {"voter": voter, "avg_score": round(total / count, 2), "votes_cast": count}
        for voter, (total, count) in sorted(voter_totals.items())
    ]

    dimensions = []
    for decision, dims in sorted(dim_totals_by_decision.items()):
        row: dict[str, str | float | None] = {"decision": decision}
        for dim in DIMENSIONS:
            total, count = dims[dim]
            row[dim] = _finalize_average(total, count)
        dimensions.append(row)

    add_scores = uniqueness_by_council_decision["add"]
    skip_scores = uniqueness_by_council_decision["skip"]
    council_overlap = {
        "add_n": len(add_scores),
        "add_avg_uniqueness": _finalize_average(sum(add_scores), len(add_scores)),
        "skip_n": len(skip_scores),
        "skip_avg_uniqueness": _finalize_average(sum(skip_scores), len(skip_scores)),
    }

    return {"counts": counts, "voters": voters, "dimensions": dimensions,
             "council_overlap": council_overlap}
