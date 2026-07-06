#!/usr/bin/env python3
"""CLI entrypoint. Dispatch only — no business logic. See architecture.md."""
import argparse
import sys

from scout import build as build_mod
from scout import eval as eval_mod
from scout import harvest_github
from scout import harvest_reddit
from scout import library
from scout.util import log_event


def cmd_harvest(args):
    result = harvest_github.run(limit=args.limit)
    if not args.github_only:
        reddit_result = harvest_reddit.run(limit=args.limit)
        result = {k: result[k] + reddit_result[k] for k in result}
    summary = f"harvest: {result['new']} new candidates, {result['seen_skipped']} already seen, {result['errors']} errors"
    print(summary)
    log_event("harvest", summary)


def cmd_build(args):
    result = build_mod.run(limit=args.limit)
    summary = f"build: {result['drafted']} drafted, {result['failed']} failed"
    print(summary)
    log_event("build", summary)


def cmd_eval(args):
    result = eval_mod.run()
    summary = f"eval: {result['passed']} passed, {result['failed']} failed"
    print(summary)
    log_event("eval", summary)


def cmd_search(args):
    matches = library.search(args.keyword_or_name)
    if not matches:
        print(f"No matches for '{args.keyword_or_name}'")
        log_event("search", f"query='{args.keyword_or_name}' matches=0")
        return
    for m in matches:
        tags = ", ".join(m.get("tags", []))
        print(f"{m.get('name')}  [{tags}]  ({m.get('source_url', '')})")
    log_event("search", f"query='{args.keyword_or_name}' matches={len(matches)}")


def cmd_show(args):
    try:
        print(library.show(args.keyword_or_name))
        log_event("show", f"name='{args.keyword_or_name}' found=true")
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        log_event("show", f"name='{args.keyword_or_name}' found=false error={exc}")
        sys.exit(1)


def cmd_review(args):
    library.review()
    log_event("review", "review session completed")


def cmd_scout(args):
    harvest_result = harvest_github.run(limit=args.limit)
    build_result = build_mod.run(limit=args.limit)
    eval_result = eval_mod.run()
    summary = (f"scout: harvested {harvest_result['new']}, built {build_result['drafted']}, "
               f"evaluated {eval_result['passed']} passed / {eval_result['failed']} failed")
    print(summary)
    log_event("scout", summary)


def main():
    parser = argparse.ArgumentParser(
        prog="claude-scout",
        description="Discover, draft, and evaluate Claude Code skills.",
    )
    parser.add_argument(
        "--mode", required=True,
        choices=["harvest", "build", "eval", "search", "show", "review", "scout"],
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
        "review": cmd_review,
        "scout": cmd_scout,
    }
    handlers[args.mode](args)


if __name__ == "__main__":
    main()
