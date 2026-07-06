from unittest.mock import MagicMock, patch

from scout import build


def _write_candidates(tmp_path, candidates_dir):
    candidates_dir.mkdir(parents=True, exist_ok=True)
    (candidates_dir / "discovery-2026-07-06.json").write_text(
        '[{"name": "example/repo", "url": "https://x/repo", "description": "d"}]'
    )


def test_skip_already_drafted(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    drafts_dir = tmp_path / "drafts"
    failed_dir = drafts_dir / "failed"
    _write_candidates(tmp_path, candidates_dir)
    (drafts_dir / "example-repo").mkdir(parents=True)

    monkeypatch.setattr(build, "CANDIDATES_DIR", candidates_dir)
    monkeypatch.setattr(build, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(build, "FAILED_DIR", failed_dir)
    monkeypatch.setattr(build, "LOGS_DIR", tmp_path / "logs")

    with patch.object(build.subprocess, "run") as mock_run:
        result = build.run()

    mock_run.assert_not_called()
    assert result == {"drafted": 0, "failed": 0}


def test_writes_draft_on_success(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    drafts_dir = tmp_path / "drafts"
    _write_candidates(tmp_path, candidates_dir)
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "build.md").write_text("Name: {name} URL: {url} Desc: {description}")

    monkeypatch.setattr(build, "CANDIDATES_DIR", candidates_dir)
    monkeypatch.setattr(build, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(build, "FAILED_DIR", drafts_dir / "failed")
    monkeypatch.setattr(build, "PROMPT_TEMPLATE", tmp_path / "prompts" / "build.md")
    monkeypatch.setattr(build, "LOGS_DIR", tmp_path / "logs")

    mock_result = MagicMock(returncode=0, stdout="---\nname: repo\ndescription: d\n---\nbody", stderr="")
    with patch.object(build.subprocess, "run", return_value=mock_result):
        result = build.run()

    assert result == {"drafted": 1, "failed": 0}
    assert (drafts_dir / "example-repo" / "SKILL.md").exists()


def test_timeout_moves_to_failed(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    drafts_dir = tmp_path / "drafts"
    _write_candidates(tmp_path, candidates_dir)
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "build.md").write_text("{name} {url} {description}")

    monkeypatch.setattr(build, "CANDIDATES_DIR", candidates_dir)
    monkeypatch.setattr(build, "DRAFTS_DIR", drafts_dir)
    monkeypatch.setattr(build, "FAILED_DIR", drafts_dir / "failed")
    monkeypatch.setattr(build, "PROMPT_TEMPLATE", tmp_path / "prompts" / "build.md")
    monkeypatch.setattr(build, "LOGS_DIR", tmp_path / "logs")

    with patch.object(build.subprocess, "run", side_effect=build.subprocess.TimeoutExpired(cmd="claude", timeout=600)):
        result = build.run()

    assert result == {"drafted": 0, "failed": 1}
    assert (drafts_dir / "failed" / "example-repo").exists()
