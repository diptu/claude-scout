"""Curation: search/show/review. Only module allowed to touch library/ and trash/."""
import datetime
import shutil

from scout.util import PROJECT_ROOT, read_json, write_json

DRAFTS_DIR = PROJECT_ROOT / "drafts"
LIBRARY_DIR = PROJECT_ROOT / "library"
TRASH_DIR = PROJECT_ROOT / "trash"
SKIP_DIR_NAMES = {"failed", "failed-reason-eval"}


def _iter_library_entries():
    if not LIBRARY_DIR.exists():
        return
    for entry in LIBRARY_DIR.iterdir():
        meta_path = entry / "meta.json"
        if meta_path.exists():
            yield entry, read_json(meta_path, default={})


def search(keyword: str) -> list:
    keyword = keyword.lower()
    matches = []
    for _, meta in _iter_library_entries():
        haystack = " ".join([meta.get("name", ""), *meta.get("tags", [])]).lower()
        if keyword in haystack:
            matches.append(meta)
    return matches


def show(name: str) -> str:
    skill_path = LIBRARY_DIR / name / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"no skill named '{name}' in library/")
    return skill_path.read_text()


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
        skill_md = (draft_dir / "SKILL.md").read_text()
        candidate = read_json(draft_dir / "candidate.json", default={})
        print(f"\n=== {draft_dir.name} ===")
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
            shutil.rmtree(draft_dir)
        elif choice == "t":
            dest = TRASH_DIR / draft_dir.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(draft_dir), str(dest))
        # "s" (skip) or any other input: leave the draft in place for next time
