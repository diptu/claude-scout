#!/usr/bin/env python3
"""
remove_legacy_skills.py
=======================

Deletes the 47 legacy skill directories now that `atlas` replaces them.

Cross-platform (Windows / Linux / macOS). Standard library only — no pip install.
Python 3.7+ required (uses pathlib).

USAGE
-----
    python remove_legacy_skills.py [options]

OPTIONS
-------
    --base-dir PATH        Directory containing the legacy skill dirs.
                           Default: C:\\Users\\diptu\\Documents\\claude-scout\\.claude\\skills
    --atlas-dir PATH       Path where the new atlas skill should exist.
                           Default: C:\\Users\\diptu\\Documents\\claude-scout\\.skills\\atlas
    --yes                  Actually delete. Without this, runs dry-run.
    --bootstrap-atlas      If atlas is missing, create a placeholder SKILL.md
                           at --atlas-dir instead of refusing to run.
    -h, --help             Show this help and exit.

EXAMPLES
--------
    # Dry-run with defaults:
    python remove_legacy_skills.py

    # Real delete:
    python remove_legacy_skills.py --yes

    # Skip the atlas check entirely (bootstrap a placeholder, then delete):
    python remove_legacy_skills.py --bootstrap-atlas --yes

    # Custom paths:
    python remove_legacy_skills.py --base-dir ./skills --atlas-dir ../.skills/atlas --yes

SAFETY
------
    * Dry-run by default. Pass --yes to mutate.
    * Asks for confirmation before mutation, even after --yes.
    * Refuses to run unless atlas exists at --atlas-dir (unless --bootstrap-atlas).
    * Idempotent: missing dirs are reported, not errored.
    * Only touches the 47 named dirs. Never a recursive wipe.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Verbatim from the legacy C:\ skill listing (47 entries).
LEGACY_SKILLS = [
    "ai-engineer",
    "autonomous-sprint-orchestator",
    "backend-event-driven",
    "backend-fastapi",
    "backend-rest-api",
    "cloud-architect",
    "coreyhaines31-marketingskills",
    "cto",
    "data-architect",
    "database-engineer",
    "database-postgresql",
    "database-redis",
    "devops-docker",
    "devops-kubernetes",
    "devops-observability",
    "devops-sre",
    "devops-terraform",
    "documentation",
    "engineering-audit",
    "engineering-code-review",
    "engineering-manager",
    "enterprise-architect",
    "frontend-accessibility",
    "frontend-performance",
    "frontend-react",
    "frontend-typescript",
    "llm-agents",
    "llm-prompt-engineering",
    "llm-rag",
    "ml-architect",
    "onvoyage-ai-gtm-engineer-skills",
    "Phase-1-Orchestrator",
    "Phase-5-Orchestrator",
    "phase-9-orchestrator",
    "product-manager",
    "qa-engineers",
    "research",
    "security-architect",
    "security-encryption",
    "security-jwt-oauth",
    "software-architect",
    "sre",
    "technical-program-manager",
    "test-automation-engineer",
    "trystan-sa-claude-design-system-prompt",
    "ui-ux-engineers",
    "ux-researcher",
]

PLACEHOLDER_ATLAS = """---
name: atlas
version: 1.0.0
description: Placeholder. Replace with the real atlas SKILL.md before relying on it.
---

# Atlas — placeholder

This file was bootstrapped by remove_legacy_skills.py to satisfy the
replacement-in-place check. Replace it with the real SKILL.md (single
router covering product, architecture, implementation, data, quality,
operations, security, and process workflows).
"""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Remove the 47 legacy skill dirs safely.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("EXAMPLES")[1] if "EXAMPLES" in __doc__ else "",
    )
    p.add_argument(
        "--base-dir",
        default=r"C:\Users\diptu\Documents\claude-scout\.claude\skills",
        help="Directory containing the legacy skill dirs (default: %(default)s)",
    )
    p.add_argument(
        "--atlas-dir",
        default=r"C:\Users\diptu\Documents\claude-scout\.skills\atlas",
        help="Path where atlas should exist (default: %(default)s)",
    )
    p.add_argument(
        "--yes",
        action="store_true",
        help="Actually delete (default: dry-run).",
    )
    p.add_argument(
        "--bootstrap-atlas",
        action="store_true",
        help="If atlas is missing, write a placeholder SKILL.md instead of refusing.",
    )
    return p.parse_args()


def ensure_atlas(atlas_dir: Path, bootstrap: bool) -> None:
    """Verify atlas exists. Bootstrap a placeholder if requested."""
    if atlas_dir.is_dir() and (atlas_dir / "SKILL.md").is_file():
        return

    if not bootstrap:
        print(f"ERROR: atlas not found at {atlas_dir}", file=sys.stderr)
        print(
            "       Pass --bootstrap-atlas to create a placeholder,",
            file=sys.stderr,
        )
        print(
            "       or --atlas-dir <path> to point at an existing copy.",
            file=sys.stderr,
        )
        sys.exit(1)

    atlas_dir.mkdir(parents=True, exist_ok=True)
    (atlas_dir / "SKILL.md").write_text(PLACEHOLDER_ATLAS, encoding="utf-8")
    print(f"Bootstrapped placeholder atlas at: {atlas_dir}")


def plan(base_dir: Path) -> tuple[list[str], list[str]]:
    """Return (existing_dirs, missing_dirs) under base_dir."""
    existing: list[str] = []
    missing: list[str] = []
    for skill in LEGACY_SKILLS:
        if (base_dir / skill).is_dir():
            existing.append(skill)
        else:
            missing.append(skill)
    return existing, missing


def main() -> None:
    args = parse_args()

    base_dir = Path(args.base_dir).expanduser().resolve()
    atlas_dir = Path(args.atlas_dir).expanduser().resolve()

    print(f"Base dir : {base_dir}")
    print(f"Atlas dir: {atlas_dir}")
    print(f"Mode     : {'EXECUTE' if args.yes else 'DRY-RUN'}")
    print()

    # Pre-flight
    if not base_dir.is_dir():
        print(f"ERROR: base dir does not exist: {base_dir}", file=sys.stderr)
        print(
            "       Pass --base-dir <path> to point at the actual directory.",
            file=sys.stderr,
        )
        sys.exit(1)

    ensure_atlas(atlas_dir, args.bootstrap_atlas)

    # Plan
    existing, missing = plan(base_dir)
    print(f"Found    : {len(existing)} of {len(LEGACY_SKILLS)}")
    print(f"Missing  : {len(missing)}")
    print()

    if not existing:
        print("Nothing to remove.")
        return

    print("Will remove:")
    for skill in existing:
        print(f"  {base_dir / skill}")
    print()

    if not args.yes:
        print("DRY-RUN — pass --yes to actually delete.")
        print(f"  Example: python {Path(__file__).name} --yes")
        return

    # Confirm
    try:
        confirm = input(
            f"Delete {len(existing)} directories under {base_dir}? [y/N]: "
        ).strip()
    except EOFError:
        print("Aborted (no input).")
        return

    if confirm.lower() != "y":
        print("Aborted.")
        return

    # Execute
    deleted = 0
    failed = 0
    for skill in existing:
        path = base_dir / skill
        try:
            shutil.rmtree(path)
            print(f"  OK  removed {skill}")
            deleted += 1
        except OSError as e:
            print(f"  ERR failed  {skill}  -- {e}")
            failed += 1

    print()
    print(f"Done. Deleted: {deleted}, Failed: {failed}")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()