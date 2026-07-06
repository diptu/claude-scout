import pytest

from scout import library


def test_search_matches_tag(tmp_path, monkeypatch):
    library_dir = tmp_path / "library"
    entry = library_dir / "skill-a"
    entry.mkdir(parents=True)
    (entry / "meta.json").write_text('{"name": "skill-a", "tags": ["python", "cli"]}')

    monkeypatch.setattr(library, "LIBRARY_DIR", library_dir)

    results = library.search("python")
    assert len(results) == 1
    assert results[0]["name"] == "skill-a"

    assert library.search("nonexistent") == []


def test_show_raises_for_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(library, "LIBRARY_DIR", tmp_path / "library")
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
    d = drafts_dir / "skill-x"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text("---\nname: skill-x\ndescription: d\n---\nbody")
    (d / ".eval_status").write_text("passed\n")
    (d / "candidate.json").write_text('{"url": "https://x/skill-x"}')

    monkeypatch.setattr(library, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(library, "LIBRARY_DIR", library_dir)
    monkeypatch.setattr(library, "TRASH_DIR", tmp_path / "trash")
    monkeypatch.setattr("builtins.input", lambda prompt="": "p" if "promote" in prompt or "?" in prompt else "")

    inputs = iter(["p", "python,cli"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    library.review()

    assert (library_dir / "skill-x" / "SKILL.md").exists()
    assert not d.exists()
