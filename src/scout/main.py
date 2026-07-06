#!/usr/bin/env python3
"""CLI entrypoint. Dispatch only — no business logic. See architecture.md."""
import argparse
import io
import sys

from scout.commands import build as build_mod
from scout.commands import committee as committee_mod
from scout.commands import eval as eval_mod
from scout.commands import library
from scout.commands import reset_harvest
from scout.core.logger import log_event
from scout.services import harvest_github, harvest_reddit


def cmd_harvest(args):
    result = harvest_github.run(limit=args.limit)
    if not args.github_only:
        reddit_result = harvest_reddit.run(limit=args.limit)
        result = {k: v + reddit_result[k] for k, v in result.items()}
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
    summary = (f"committee: {result['hired']} hired, {result['rejected']} rejected, "
               f"{result['no_quorum']} no-quorum, {result['collisions']} name-collisions")
    print(summary)
    log_event("committee", summary)


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
               f"committee {committee_result['hired']} hired / {committee_result['rejected']} "
               f"rejected / {committee_result['no_quorum']} no-quorum / "
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
        choices=["harvest", "build", "eval", "committee", "search", "show", "review", "scout",
                 "reset-harvest"],
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
        "review": cmd_review,
        "scout": cmd_scout,
        "reset-harvest": cmd_reset_harvest,
    }
    handlers[args.mode](args)


if __name__ == "__main__":
    main()
