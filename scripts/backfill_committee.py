#!/usr/bin/env python3
"""One-off backfill: score existing library/ entries that predate the
committee gate (or were promoted via manual library.review()) with real
committee votes, so scout/commands/digest.py has something besides
date_added to rank them by.

Run once by hand: make backfill (or `PYTHONPATH=src python3 scripts/backfill_committee.py`)

Safe to re-run: any entry that already has a committee_verdict.json is
skipped with zero `claude` CLI calls, so a partial run (killed mid-way, or
entries that came back no-quorum) can simply be re-invoked to mop up the
rest without re-voting on already-scored entries.

Deliberately never imports _promote/_reject/run() from committee.py: this
script only ever adds committee_score/committee_verdict.json to existing
library/<name>/ entries. It never touches drafts/, trash/, or committee.py's
library/-name-collision guard (nothing to collide with here — this script
targets already-curated library/ entries directly, not drafts/).

Backfilled scores are informational only: even a score below passing_score
never moves an entry to trash/ or otherwise changes its status. If a low
score bothers you, that's a manual `library/` decision, not this script's."""
# pylint: disable=protected-access
from scout.commands.committee import _cast_votes, _committee_config, _overall_score
from scout.core.config import PROJECT_ROOT
from scout.core.util import read_json, write_json

LIBRARY_DIR = PROJECT_ROOT / "library"


def run() -> dict:
    _, min_voters, voters = _committee_config()
    entries = sorted(
        (e for e in LIBRARY_DIR.iterdir() if e.is_dir()),
        key=lambda p: p.name,
    ) if LIBRARY_DIR.exists() else []

    scored = 0
    skipped = 0
    no_quorum = 0
    unreadable = 0

    for entry in entries:
        verdict_path = entry / "committee_verdict.json"
        if verdict_path.exists():
            skipped += 1
            continue

        skill_md_path = entry / "SKILL.md"
        if not skill_md_path.exists():
            print(f"  -> {entry.name}: no SKILL.md, skipping")
            unreadable += 1
            continue
        try:
            skill_md = skill_md_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"  -> {entry.name}: unreadable ({exc}), skipping")
            unreadable += 1
            continue

        print(f"backfilling {entry.name} ...", flush=True)
        log_lines: list[str] = []
        votes = _cast_votes(skill_md, voters, log_lines, exclude_name=entry.name)

        if len(votes) < min_voters:
            no_quorum += 1
            print(f"  -> no quorum ({len(votes)}/{len(voters)} voted) — re-run this script "
                  "later to retry just this entry")
            continue

        overall = round(_overall_score(votes), 2)
        passing_score, _, _ = _committee_config()
        verdict = {
            "overall_score": overall,
            "passing_score": passing_score,
            "decision": "backfilled",
            "votes": votes,
        }
        write_json(verdict_path, verdict)

        # Merge, never overwrite: existing entries carry hand-set tags/
        # source_url/date_added from library.review() that a fresh-dict
        # write (like committee.py's _promote()) would silently wipe.
        meta = read_json(entry / "meta.json", default={})
        meta["committee_score"] = overall
        meta["committee_decision"] = "backfilled"
        write_json(entry / "meta.json", meta)

        scored += 1
        print(f"  -> scored {overall}/5 ({len(votes)}/{len(voters)} voted)")

    return {"scored": scored, "skipped": skipped, "no_quorum": no_quorum, "unreadable": unreadable}


if __name__ == "__main__":
    result = run()
    print(
        f"\nbackfill: {result['scored']} scored, {result['skipped']} already had a verdict, "
        f"{result['no_quorum']} no-quorum, {result['unreadable']} unreadable"
    )
