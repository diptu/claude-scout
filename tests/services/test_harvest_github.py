from unittest.mock import MagicMock, patch

from scout.services import harvest_github


def _mock_response(items):
    resp = MagicMock()
    resp.json.return_value = {"items": items}
    resp.headers = {"X-RateLimit-Remaining": "100"}
    resp.raise_for_status.return_value = None
    return resp


def test_dedupe_skips_seen_url(tmp_path, monkeypatch):
    monkeypatch.setattr(harvest_github, "CANDIDATES_DIR", tmp_path)
    monkeypatch.setattr(harvest_github, "SEEN_FILE", tmp_path / "seen.txt")
    monkeypatch.setattr(harvest_github, "LIBRARY_DIR", tmp_path / "library")
    monkeypatch.setattr(harvest_github, "load_config", lambda: {})
    (tmp_path / "seen.txt").write_text("https://github.com/example/already-seen\n")

    item = {
        "html_url": "https://github.com/example/already-seen",
        "full_name": "example/already-seen",
        "description": "desc",
        "stargazers_count": 100,
    }
    with patch.object(harvest_github.requests, "get", return_value=_mock_response([item])):
        result = harvest_github.run(limit=10)

    assert result["new"] == 0
    assert result["seen_skipped"] >= 1


def test_records_new_candidates_and_seen(tmp_path, monkeypatch):
    monkeypatch.setattr(harvest_github, "CANDIDATES_DIR", tmp_path)
    monkeypatch.setattr(harvest_github, "SEEN_FILE", tmp_path / "seen.txt")
    monkeypatch.setattr(harvest_github, "LIBRARY_DIR", tmp_path / "library")
    monkeypatch.setattr(harvest_github, "load_config", lambda: {})

    item = {
        "html_url": "https://github.com/example/new-repo",
        "full_name": "example/new-repo",
        "description": "desc",
        "stargazers_count": 100,
    }
    with patch.object(harvest_github.requests, "get", return_value=_mock_response([item])):
        result = harvest_github.run(limit=10)

    assert result["new"] == 1
    assert "https://github.com/example/new-repo" in (tmp_path / "seen.txt").read_text()


def test_api_failure_increments_errors_not_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(harvest_github, "CANDIDATES_DIR", tmp_path)
    monkeypatch.setattr(harvest_github, "SEEN_FILE", tmp_path / "seen.txt")
    monkeypatch.setattr(harvest_github, "LIBRARY_DIR", tmp_path / "library")
    monkeypatch.setattr(harvest_github, "load_config", lambda: {})

    with patch.object(harvest_github.requests, "get", side_effect=harvest_github.requests.RequestException("boom")):
        result = harvest_github.run(limit=10)

    assert result["errors"] == len(harvest_github.KEYWORDS)
    assert result["new"] == 0


def test_dedupe_skips_url_already_in_library(tmp_path, monkeypatch):
    """A reset-harvest wipes seen.txt, but re-harvesting shouldn't re-add
    skills already promoted to library/."""
    monkeypatch.setattr(harvest_github, "CANDIDATES_DIR", tmp_path)
    monkeypatch.setattr(harvest_github, "SEEN_FILE", tmp_path / "seen.txt")
    library_dir = tmp_path / "library"
    monkeypatch.setattr(harvest_github, "LIBRARY_DIR", library_dir)
    monkeypatch.setattr(harvest_github, "load_config", lambda: {})
    entry = library_dir / "already-curated"
    entry.mkdir(parents=True)
    (entry / "meta.json").write_text(
        '{"name": "already-curated", "source_url": "https://github.com/example/already-curated"}'
    )

    item = {
        "html_url": "https://github.com/example/already-curated",
        "full_name": "example/already-curated",
        "description": "desc",
        "stargazers_count": 100,
    }
    with patch.object(harvest_github.requests, "get", return_value=_mock_response([item])):
        result = harvest_github.run(limit=10)

    assert result["new"] == 0
    assert result["seen_skipped"] >= 1
    assert not (tmp_path / "seen.txt").exists()
