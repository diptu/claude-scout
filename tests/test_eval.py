from scout import eval as eval_mod


def _make_draft(drafts_dir, name, content):
    d = drafts_dir / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(content)
    return d


def test_skip_already_evaluated(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    d = _make_draft(drafts_dir, "a", "---\nname: a\ndescription: d\n---\nbody")
    (d / ".eval_status").write_text("passed\n")

    monkeypatch.setattr(eval_mod, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(eval_mod, "FAILED_EVAL_DIR", drafts_dir / "failed-reason-eval")
    monkeypatch.setattr(eval_mod, "_claude_available", lambda: False)

    result = eval_mod.run()

    assert result == {"passed": 0, "failed": 0}


def test_missing_frontmatter_fails_without_calling_claude(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "b", "no frontmatter here")

    monkeypatch.setattr(eval_mod, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(eval_mod, "FAILED_EVAL_DIR", drafts_dir / "failed-reason-eval")
    monkeypatch.setattr(eval_mod, "_claude_available", lambda: True)

    calls = []
    monkeypatch.setattr(eval_mod.subprocess, "run", lambda *a, **k: calls.append(1))

    result = eval_mod.run()

    assert result == {"passed": 0, "failed": 1}
    assert calls == []
    assert (drafts_dir / "failed-reason-eval" / "b").exists()


def test_frontmatter_only_pass_when_claude_unavailable(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "c", "---\nname: c\ndescription: d\n---\nbody")

    monkeypatch.setattr(eval_mod, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(eval_mod, "FAILED_EVAL_DIR", drafts_dir / "failed-reason-eval")
    monkeypatch.setattr(eval_mod, "_claude_available", lambda: False)

    result = eval_mod.run()

    assert result == {"passed": 1, "failed": 0}
    assert (drafts_dir / "c" / ".eval_status").read_text().strip() == "passed"
