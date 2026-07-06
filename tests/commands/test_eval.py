from unittest.mock import MagicMock

from scout.commands import eval as eval_mod


def _make_draft(drafts_dir, name, content):
    d = drafts_dir / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(content)
    return d


def _canned_claude(answers):
    """Mimic subprocess.run for claude calls, returning canned stdouts in order."""
    answer_iter = iter(answers)

    def fake_run(*_args, **_kwargs):
        return MagicMock(returncode=0, stdout=next(answer_iter), stderr="")

    return fake_run


def _patch_dirs(monkeypatch, tmp_path, drafts_dir):
    monkeypatch.setattr(eval_mod, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(eval_mod, "FAILED_EVAL_DIR", drafts_dir / "failed-reason-eval")
    monkeypatch.setattr(eval_mod, "LOGS_DIR", tmp_path / "logs")


def test_skip_already_evaluated(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    d = _make_draft(drafts_dir, "a", "---\nname: a\ndescription: d\n---\nbody")
    (d / ".eval_status").write_text("passed\n")

    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    monkeypatch.setattr(eval_mod, "_claude_available", lambda: False)

    result = eval_mod.run()

    assert result["passed"] == 0
    assert result["failed"] == 0
    assert result["report"] == []


def test_missing_frontmatter_fails_without_calling_claude(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "b", "no frontmatter here")

    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    monkeypatch.setattr(eval_mod, "_claude_available", lambda: True)

    calls = []
    monkeypatch.setattr(eval_mod.subprocess, "run", lambda *a, **k: calls.append(1))

    result = eval_mod.run()

    assert result["passed"] == 0
    assert result["failed"] == 1
    assert calls == []
    assert (drafts_dir / "failed-reason-eval" / "b").exists()
    assert result["report"] == [
        {"name": "b", "battery": "-", "tests": 0, "result": "failed"},
    ]


def test_frontmatter_only_pass_when_claude_unavailable(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "c", "---\nname: c\ndescription: d\n---\nbody")

    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    monkeypatch.setattr(eval_mod, "_claude_available", lambda: False)

    result = eval_mod.run()

    assert result["passed"] == 1
    assert result["failed"] == 0
    assert (drafts_dir / "c" / ".eval_status").read_text().strip() == "passed"
    assert result["report"] == [
        {"name": "c", "battery": "frontmatter-only", "tests": 0, "result": "passed"},
    ]


def test_standard_battery_when_verify_says_applicable(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "d", "---\nname: d\ndescription: x\n---\nbody")
    prompts_file = tmp_path / "eval_tests.md"
    prompts_file.write_text('1. "Generic test one."\n2. "Generic test two."\n')

    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    monkeypatch.setattr(eval_mod, "EVAL_PROMPTS_FILE", prompts_file)
    monkeypatch.setattr(eval_mod, "_claude_available", lambda: True)
    # 1 verify answer + 2 standard test answers
    monkeypatch.setattr(eval_mod.subprocess, "run",
                        _canned_claude(["APPLICABLE", "ok", "ok"]))

    result = eval_mod.run()

    assert result["passed"] == 1
    assert result["report"] == [
        {"name": "d", "battery": "standard", "tests": 2, "result": "passed"},
    ]


def test_custom_test_designed_when_battery_not_applicable(tmp_path, monkeypatch):
    drafts_dir = tmp_path / "drafts"
    _make_draft(drafts_dir, "e", "---\nname: e\ndescription: x\n---\nbody")
    prompts_file = tmp_path / "eval_tests.md"
    prompts_file.write_text('1. "Generic test one."\n2. "Generic test two."\n')

    _patch_dirs(monkeypatch, tmp_path, drafts_dir)
    monkeypatch.setattr(eval_mod, "EVAL_PROMPTS_FILE", prompts_file)
    monkeypatch.setattr(eval_mod, "_claude_available", lambda: True)
    # verify answer is a tailored replacement test, then 1 answer for that test
    monkeypatch.setattr(eval_mod.subprocess, "run",
                        _canned_claude(["Ask the skill to do its one thing.", "ok"]))

    result = eval_mod.run()

    assert result["passed"] == 1
    assert result["report"] == [
        {"name": "e", "battery": "custom", "tests": 1, "result": "passed"},
    ]
    # the designed test is captured in the eval log for auditability
    log_file = next((tmp_path / "logs").glob("eval-*-e.log"))
    assert "Ask the skill to do its one thing." in log_file.read_text(encoding="utf-8")
