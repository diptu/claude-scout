from unittest.mock import MagicMock, patch

from scout.services import harvest_tiktok


def _patch_dirs(monkeypatch, tmp_path):
    monkeypatch.setattr(harvest_tiktok, "CANDIDATES_DIR", tmp_path)
    monkeypatch.setattr(harvest_tiktok, "SEEN_FILE", tmp_path / "seen.txt")
    monkeypatch.setattr(harvest_tiktok, "LIBRARY_DIR", tmp_path / "library")
    monkeypatch.setattr(harvest_tiktok, "load_config", lambda: {})
    monkeypatch.setenv("TIKTOK_CLIENT_KEY", "test-key")
    monkeypatch.setenv("TIKTOK_CLIENT_SECRET", "test-secret")


def _video(video_id="1", username="creator", views=5000, description="a claude skill demo"):
    return {
        "id": video_id,
        "username": username,
        "view_count": views,
        "video_description": description,
    }


def _fake_post(videos, token="test-access-token"):
    def fake_post(url, params=None, json=None, data=None, headers=None, timeout=None):  # noqa: ARG001
        resp = MagicMock()
        resp.raise_for_status.return_value = None
        if url == harvest_tiktok.TOKEN_URL:
            resp.json.return_value = {"access_token": token}
        elif url == harvest_tiktok.QUERY_URL:
            resp.json.return_value = {"data": {"videos": videos}}
        return resp
    return fake_post


def test_no_op_without_credentials(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)
    monkeypatch.delenv("TIKTOK_CLIENT_KEY", raising=False)
    monkeypatch.delenv("TIKTOK_CLIENT_SECRET", raising=False)

    result = harvest_tiktok.run(limit=10)

    assert result == {"new": 0, "seen_skipped": 0, "errors": 0}


def test_dedupe_skips_seen_url(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)
    (tmp_path / "seen.txt").write_text("https://www.tiktok.com/@creator/video/1\n")

    with patch.object(harvest_tiktok.requests, "post", side_effect=_fake_post([_video()])):
        result = harvest_tiktok.run(limit=10)

    assert result["new"] == 0
    assert result["seen_skipped"] >= 1


def test_records_new_candidates_and_seen(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)

    with patch.object(harvest_tiktok.requests, "post", side_effect=_fake_post([_video()])):
        result = harvest_tiktok.run(limit=10)

    assert result["new"] == 1
    assert "https://www.tiktok.com/@creator/video/1" in (tmp_path / "seen.txt").read_text()


def test_views_below_threshold_is_skipped(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)
    low_views = _video(views=10)

    with patch.object(harvest_tiktok.requests, "post", side_effect=_fake_post([low_views])):
        result = harvest_tiktok.run(limit=10)

    assert result["new"] == 0


def test_token_fetch_failure_increments_errors_not_raises(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)

    with patch.object(harvest_tiktok.requests, "post",
                       side_effect=harvest_tiktok.requests.RequestException("boom")):
        result = harvest_tiktok.run(limit=10)

    assert result == {"new": 0, "seen_skipped": 0, "errors": 1}
