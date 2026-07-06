import pytest

from scout.commands import library


def test_search_matches_tag(tmp_path, monkeypatch):
    library_dir = tmp_path / "library"
    entry = library_dir / "skill-a"
    entry.mkdir(parents=True)
    (entry / "meta.json").write_text('{"name": "skill-a", "tags": ["python", "cli"]}')

    monkeypatch.setattr(library, "LIBRARY_DIR", library_dir)
    monkeypatch.setattr(library, "SKILLS_DIR", tmp_path / "skills")

    results = library.search("python")
    assert len(results) == 1
    assert results[0]["name"] == "skill-a"

    assert library.search("nonexistent") == []


def test_search_finds_local_skill_by_name(tmp_path, monkeypatch):
    skills_dir = tmp_path / ".claude" / "skills"
    entry = skills_dir / "ai-engineer"
    entry.mkdir(parents=True)
    (entry / "SKILL.md").write_text(
        "---\nname: ai-engineer\ndescription: Build production-grade AI features.\n---\nbody",
        encoding="utf-8",
    )

    monkeypatch.setattr(library, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(library, "LIBRARY_DIR", tmp_path / "library")
    monkeypatch.setattr(library, "SKILLS_DIR", skills_dir)

    results = library.search("ai-engineer")
    assert len(results) == 1
    assert results[0]["name"] == "ai-engineer"
    assert results[0]["description"] == "Build production-grade AI features."

    # description text is searchable too
    assert library.search("production-grade")[0]["name"] == "ai-engineer"


def test_show_falls_back_to_local_skills(tmp_path, monkeypatch):
    skills_dir = tmp_path / ".claude" / "skills"
    entry = skills_dir / "ai-engineer"
    entry.mkdir(parents=True)
    (entry / "SKILL.md").write_text("skill body \U0001f9e0", encoding="utf-8")

    monkeypatch.setattr(library, "LIBRARY_DIR", tmp_path / "library")
    monkeypatch.setattr(library, "SKILLS_DIR", skills_dir)

    assert library.show("ai-engineer") == "skill body \U0001f9e0"


def test_show_raises_for_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(library, "LIBRARY_DIR", tmp_path / "library")
    monkeypatch.setattr(library, "SKILLS_DIR", tmp_path / "skills")
    with pytest.raises(FileNotFoundError):
        library.show("nope")


def test_review_only_lists_passed(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    passed = drafts_dir / "passed-one"
    passed.mkdir(parents=True)
    (passed / "SKILL.md").write_text("---\nname: p\ndescription: d\n---\nbody")
    (passed / ".eval_status").write_text("passed\n")

    not_evaluated = drafts_dir / "not-evaluated"
    not_evaluated.mkdir(parents=True)
    (not_evaluated / "SKILL.md").write_text("---\nname: n\ndescription: d\n---\nbody")

    monkeypatch.setattr(library, "DRAFTS_DIR", drafts_dir)

    assert [d.name for d in library._passed_drafts()] == ["passed-one"]


def test_review_promote_moves_to_library(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    library_dir = tmp_path / "library"
    skills_dir = tmp_path / "skills"
    d = drafts_dir / "skill-x"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text("---\nname: skill-x\ndescription: d\n---\nbody")
    (d / ".eval_status").write_text("passed\n")
    (d / "candidate.json").write_text('{"url": "https://x/skill-x"}')

    monkeypatch.setattr(library, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(library, "LIBRARY_DIR", library_dir)
    monkeypatch.setattr(library, "TRASH_DIR", tmp_path / "trash")
    monkeypatch.setattr(library, "SKILLS_DIR", skills_dir)

    inputs = iter(["p", "python,cli", "n"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    library.review()

    assert (library_dir / "skill-x" / "SKILL.md").exists()
    assert not d.exists()
    assert not (skills_dir / "skill-x").exists()


def test_review_promote_can_also_add_to_claude_skills(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    library_dir = tmp_path / "library"
    skills_dir = tmp_path / "skills"
    d = drafts_dir / "skill-y"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text("---\nname: skill-y\ndescription: d\n---\nbody")
    (d / ".eval_status").write_text("passed\n")
    (d / "candidate.json").write_text('{"url": "https://x/skill-y"}')

    monkeypatch.setattr(library, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(library, "LIBRARY_DIR", library_dir)
    monkeypatch.setattr(library, "TRASH_DIR", tmp_path / "trash")
    monkeypatch.setattr(library, "SKILLS_DIR", skills_dir)

    inputs = iter(["p", "", "y"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    library.review()

    assert (library_dir / "skill-y" / "SKILL.md").exists()
    assert (skills_dir / "skill-y" / "SKILL.md").read_text() == \
        (library_dir / "skill-y" / "SKILL.md").read_text()
