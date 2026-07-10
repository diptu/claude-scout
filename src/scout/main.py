#!/usr/bin/env python3
"""CLI entrypoint. Dispatch only — no business logic. See architecture.md."""
import argparse
import io
import sys

from scout.commands import build as build_mod
from scout.commands import committee as committee_mod
from scout.commands import digest as digest_mod
from scout.commands import eval as eval_mod
from scout.commands import insights as insights_mod
from scout.commands import library
from scout.commands import reset_harvest
from scout.core.logger import log_event
from scout.services import (harvest_github, harvest_reddit, harvest_tiktok, harvest_twitter,
                             harvest_youtube)

NON_GITHUB_SOURCES = (harvest_reddit, harvest_twitter, harvest_youtube, harvest_tiktok)


def cmd_harvest(args):
    result = harvest_github.run(limit=args.limit)
    if not args.github_only:
        for source in NON_GITHUB_SOURCES:
            source_result = source.run(limit=args.limit)
            result = {k: v + source_result[k] for k, v in result.items()}
    summary = (f"harvest: {result['new']} new candidates, "
               f"{result['seen_skipped']} already seen, {result['errors']} errors")
    print(summary)
    log_event("harvest", summary)


def cmd_build(args):
    result = build_mod.run(limit=args.limit)
    summary = f"build: {result['drafted']} drafted, {result['failed']} failed"
    print(summary)
    log_event("build", summary)


def _one_line(text: str, width: int = 100) -> str:
    text = " ".join(text.split())
    if len(text) <= width:
        return text
    return text[: width - 1].rstrip() + "…"


def _print_eval_report(rows, reason_width: int = 50):
    if not rows:
        return
    name_w = max(len("skill"), *(len(r["name"]) for r in rows))
    battery_w = max(len("battery"), *(len(r["battery"]) for r in rows))
    reasons = [_one_line(r.get("reason", ""), reason_width) for r in rows]
    reason_w = max(len("reason"), *(len(r) for r in reasons))
    print("\nEval report:")
    print(f"| {'skill':<{name_w}} | {'battery':<{battery_w}} "
          f"| tests | result | {'reason':<{reason_w}} |")
    print(f"|{'-' * (name_w + 2)}|{'-' * (battery_w + 2)}|-------|--------|{'-' * (reason_w + 2)}|")
    for r in rows:
        reason = _one_line(r.get("reason", ""), reason_width)
        print(f"| {r['name']:<{name_w}} | {r['battery']:<{battery_w}} "
              f"| {r['tests']:>5} | {r['result']:<6} | {reason:<{reason_w}} |")
    print()


def cmd_eval(_args):
    result = eval_mod.run()
    _print_eval_report(result["report"])
    summary = f"eval: {result['passed']} passed, {result['failed']} failed"
    print(summary)
    log_event("eval", summary)


def _print_committee_report(rows):
    if not rows:
        return
    name_w = max(len("skill"), *(len(r["name"]) for r in rows))
    decision_w = max(len("decision"), *(len(r["decision"]) for r in rows))
    print("\nCommittee report:")
    print(f"| {'skill':<{name_w}} | votes | score | {'decision':<{decision_w}} |")
    print(f"|{'-' * (name_w + 2)}|-------|-------|{'-' * (decision_w + 2)}|")
    for r in rows:
        score = f"{r['score']:.2f}" if r["score"] is not None else "-"
        print(f"| {r['name']:<{name_w}} | {r['votes']:>5} | {score:>5} "
              f"| {r['decision']:<{decision_w}} |")
    print()


def cmd_committee(_args):
    result = committee_mod.run()
    _print_committee_report(result["report"])
    summary = (f"committee: {result['pending_review']} pending review, "
               f"{result['rejected']} rejected, {result['duplicate']} duplicate (council), "
               f"{result['no_quorum']} no-quorum, {result['collisions']} name-collisions, "
               f"{result['already_decided']} already-decided")
    print(summary)
    log_event("committee", summary)


def _fmt_score(value):
    return f"{value:.2f}" if value is not None else "-"


def _print_insights_report(result):
    counts = result["counts"]
    if not counts:
        print("\nno committee_verdict.json found yet in drafts/, trash/, or library/ — "
              "run `make committee` first")
        return

    print("\nDecision funnel (from committee_verdict.json / council_verdict.json on disk):")
    for bucket, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {bucket:<20} {n}")

    voters = result["voters"]
    if voters:
        name_w = max(len("voter"), *(len(v["voter"]) for v in voters))
        print("\nPer-voter average score (mean across usefulness/uniqueness/quality/safety):")
        print(f"| {'voter':<{name_w}} | avg score | votes cast |")
        print(f"|{'-' * (name_w + 2)}|-----------|------------|")
        for v in voters:
            print(f"| {v['voter']:<{name_w}} | {v['avg_score']:>9} | {v['votes_cast']:>10} |")

    dims = result["dimensions"]
    if dims:
        decision_w = max(len("decision"), *(len(row["decision"]) for row in dims))
        print("\nPer-dimension average by committee decision:")
        print(f"| {'decision':<{decision_w}} | usefulness | uniqueness | quality | safety |")
        print(f"|{'-' * (decision_w + 2)}|------------|------------|---------|--------|")
        for row in dims:
            print(f"| {row['decision']:<{decision_w}} | {_fmt_score(row['usefulness']):>10} "
                  f"| {_fmt_score(row['uniqueness']):>10} | {_fmt_score(row['quality']):>7} "
                  f"| {_fmt_score(row['safety']):>6} |")

    overlap = result["council_overlap"]
    if overlap["add_n"] or overlap["skip_n"]:
        print("\nCommittee uniqueness score vs. council's later add/skip call "
              "(tests whether the two gates actually diverge):")
        print(f"  council 'add'  (n={overlap['add_n']}): "
              f"avg committee uniqueness = {_fmt_score(overlap['add_avg_uniqueness'])}")
        print(f"  council 'skip' (n={overlap['skip_n']}): "
              f"avg committee uniqueness = {_fmt_score(overlap['skip_avg_uniqueness'])}")
    print()


def cmd_insights(_args):
    result = insights_mod.run()
    _print_insights_report(result)
    log_event("insights", f"counts={result['counts']}")


def _print_digest_report(result):
    rows = result["rows"]
    if not rows:
        print("\nno skills in library/ yet — run `make scout` first")
        return
    descriptions = [_one_line(r["description"], 50) for r in rows]
    name_w = max(len("skill"), *(len(r["name"]) for r in rows))
    desc_w = max(len("description"), *(len(d) for d in descriptions))
    print(f"\nTop {len(rows)} of {result['total']} library skill(s):")
    print(f"| {'skill':<{name_w}} | score | {'description':<{desc_w}} | source |")
    print(f"|{'-' * (name_w + 2)}|-------|{'-' * (desc_w + 2)}|--------|")
    for r, desc in zip(rows, descriptions):
        score = f"{r['score']:.2f}" if r["score"] is not None else "-"
        print(f"| {r['name']:<{name_w}} | {score:>5} | {desc:<{desc_w}} | {r['source_url']} |")
    print()


def cmd_digest(_args):
    result = digest_mod.run()
    _print_digest_report(result)
    summary = f"digest: showed {len(result['rows'])} of {result['total']} library entries"
    print(summary)
    log_event("digest", summary)


def cmd_search(args):
    query = args.keyword_or_name
    matches = library.search(query)
    if not matches:
        print(f"No skills matching '{query}' in library/ or .claude/skills/.")
        print("Tip: matching is by substring — try a shorter or broader keyword.")
        log_event("search", f"query='{query}' matches=0")
        return
    plural = "" if len(matches) == 1 else "s"
    print(f"Found {len(matches)} skill{plural} matching '{query}':\n")
    for m in matches:
        print(f"  {m.get('name')}")
        if m.get("description"):
            print(f"      {_one_line(m['description'])}")
        if m.get("tags"):
            print(f"      tags: {', '.join(m['tags'])}")
        if m.get("source_url"):
            print(f"      from: {m['source_url']}")
        print()
    print("Run `claude-scout --mode show <name>` to view a skill in full.")
    log_event("search", f"query='{query}' matches={len(matches)}")


def cmd_show(args):
    try:
        print(library.show(args.keyword_or_name))
        log_event("show", f"name='{args.keyword_or_name}' found=true")
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        log_event("show", f"name='{args.keyword_or_name}' found=false error={exc}")
        sys.exit(1)


def cmd_review(_args):
    library.review()
    log_event("review", "review session completed")


def cmd_reset_harvest(_args):
    result = reset_harvest.run()
    log_event(
        "reset-harvest",
        f"removed {result['discovery_files_removed']} discovery file(s), "
        f"seen_removed={result['seen_removed']}",
    )


def cmd_scout(args):
    harvest_result = harvest_github.run(limit=args.limit)
    build_result = build_mod.run(limit=args.limit)
    eval_result = eval_mod.run()
    _print_eval_report(eval_result["report"])
    committee_result = committee_mod.run()
    _print_committee_report(committee_result["report"])
    summary = (f"scout: harvested {harvest_result['new']}, built {build_result['drafted']}, "
               f"evaluated {eval_result['passed']} passed / {eval_result['failed']} failed, "
               f"committee {committee_result['pending_review']} pending review / "
               f"{committee_result['rejected']} rejected / "
               f"{committee_result['duplicate']} duplicate (council) / "
               f"{committee_result['no_quorum']} no-quorum / "
               f"{committee_result['collisions']} name-collisions")
    print(summary)
    log_event("scout", summary)


def main():
    # Windows consoles/pipes default to a legacy codepage (e.g. cp1252) that
    # can't encode skill content; --mode show would crash printing it.
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        prog="claude-scout",
        description="Discover, draft, and evaluate Claude Code skills.",
    )
    parser.add_argument(
        "--mode", required=True,
        choices=["harvest", "build", "eval", "committee", "insights", "digest", "search", "show",
                 "review", "scout", "reset-harvest"],
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--github-only", action="store_true")
    parser.add_argument(
        "keyword_or_name", nargs="?", default=None,
        help="keyword for search, name for show",
    )
    args = parser.parse_args()

    if args.mode == "search":
        if not args.keyword_or_name:
            print("error: search requires a keyword", file=sys.stderr)
            sys.exit(1)
        cmd_search(args)
        return
    if args.mode == "show":
        if not args.keyword_or_name:
            print("error: show requires a name", file=sys.stderr)
            sys.exit(1)
        cmd_show(args)
        return

    handlers = {
        "harvest": cmd_harvest,
        "build": cmd_build,
        "eval": cmd_eval,
        "committee": cmd_committee,
        "insights": cmd_insights,
        "digest": cmd_digest,
        "review": cmd_review,
        "scout": cmd_scout,
        "reset-harvest": cmd_reset_harvest,
    }
    handlers[args.mode](args)


if __name__ == "__main__":
    main()
