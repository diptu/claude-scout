"""Curation: search/show/review. Only module allowed to touch library/ and trash/.
search/show also read the repo's local .claude/skills/ directory, so specific
skills like `ai-engineer` are findable alongside promoted ones. review() is the
only place that writes into .claude/skills/, and only when the user opts in
while promoting a draft."""
import datetime
import re
import shutil

from scout.core.config import PROJECT_ROOT
from scout.core.util import read_json, write_json

DRAFTS_DIR = PROJECT_ROOT / "drafts"
LIBRARY_DIR = PROJECT_ROOT / "library"
SKILLS_DIR = PROJECT_ROOT / ".claude" / "skills"
TRASH_DIR = PROJECT_ROOT / "trash"
SKIP_DIR_NAMES = {"failed", "failed-reason-eval"}

DESCRIPTION_RE = re.compile(r"^description:\s*(.+)$", re.MULTILINE)


def _iter_library_entries():
    if not LIBRARY_DIR.exists():
        return
    for entry in LIBRARY_DIR.iterdir():
        meta_path = entry / "meta.json"
        if meta_path.exists():
            yield entry, read_json(meta_path, default={})


def _skill_description(skill_md) -> str:
    """First `description:` frontmatter line, else the first non-empty line.
    utf-8 with errors="replace": these files are third-party-ish and may
    contain emoji that the Windows locale codec would choke on."""
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    match = DESCRIPTION_RE.search(text)
    if match:
        return match.group(1).strip()
    for line in text.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped and stripped != "---":
            return stripped
    return ""


def _iter_skills_entries():
    """Local .claude/skills/ entries, normalized to the same meta shape as
    library/ entries (no meta.json there — name comes from the directory,
    description from SKILL.md frontmatter)."""
    if not SKILLS_DIR.exists():
        return
    for entry in sorted(SKILLS_DIR.iterdir()):
        skill_md = entry / "SKILL.md"
        if entry.is_dir() and skill_md.exists():
            yield entry, {
                "name": entry.name,
                "tags": [],
                "description": _skill_description(skill_md),
                "source_url": str(skill_md.relative_to(PROJECT_ROOT)),
            }


def search(keyword: str) -> list:
    keyword = keyword.lower()
    matches = []
    for _, meta in (*_iter_library_entries(), *_iter_skills_entries()):
        haystack = " ".join([
            meta.get("name", ""),
            meta.get("description", ""),
            *meta.get("tags", []),
        ]).lower()
        if keyword in haystack:
            matches.append(meta)
    return matches


def show(name: str) -> str:
    for base in (LIBRARY_DIR, SKILLS_DIR):
        skill_path = base / name / "SKILL.md"
        if skill_path.exists():
            return skill_path.read_text(encoding="utf-8", errors="replace")
    raise FileNotFoundError(f"no skill named '{name}' in library/ or .claude/skills/")


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


def review() -> None:
    drafts = _passed_drafts()
    if not drafts:
        print("No drafts awaiting review.")
        return

    for draft_dir in drafts:
        skill_md = (draft_dir / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        candidate = read_json(draft_dir / "candidate.json", default={})
        print(f"\n=== {draft_dir.name} ===")
        committee_verdict = read_json(draft_dir / "committee_verdict.json", default=None)
        if committee_verdict:
            print(f"committee: hired at {committee_verdict.get('overall_score')}/5")
        council_verdict = read_json(draft_dir / "council_verdict.json", default=None)
        if council_verdict:
            print(f"council: {council_verdict.get('decision')} — {council_verdict.get('reason')}")
        print(skill_md[:400])
        choice = input("[p]romote / [t]rash / [s]kip / [q]uit? ").strip().lower()

        if choice == "q":
            break
        if choice == "p":
            tags_input = input("tags (comma-separated, optional): ").strip()
            dest = LIBRARY_DIR / draft_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(draft_dir / "SKILL.md", dest / "SKILL.md")
            write_json(dest / "meta.json", {
                "name": draft_dir.name,
                "tags": [t.strip() for t in tags_input.split(",") if t.strip()],
                "source_url": candidate.get("url", ""),
                "date_added": datetime.date.today().isoformat(),
                "eval_status": "passed",
            })
            also_skills = input("also add to .claude/skills/? [y/N] ").strip().lower()
            if also_skills == "y":
                skills_dest = SKILLS_DIR / draft_dir.name
                skills_dest.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(dest / "SKILL.md", skills_dest / "SKILL.md")
                print(f"  -> also added to .claude/skills/{draft_dir.name}")
            shutil.rmtree(draft_dir)
        elif choice == "t":
            dest = TRASH_DIR / draft_dir.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(draft_dir), str(dest))
        # "s" (skip) or any other input: leave the draft in place for next time
