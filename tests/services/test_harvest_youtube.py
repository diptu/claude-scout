from unittest.mock import MagicMock, patch

from scout.services import harvest_youtube


def _patch_dirs(monkeypatch, tmp_path):
    monkeypatch.setattr(harvest_youtube, "CANDIDATES_DIR", tmp_path)
    monkeypatch.setattr(harvest_youtube, "SEEN_FILE", tmp_path / "seen.txt")
    monkeypatch.setattr(harvest_youtube, "LIBRARY_DIR", tmp_path / "library")
    monkeypatch.setattr(harvest_youtube, "load_config", lambda: {})
    monkeypatch.setenv("YOUTUBE_API_KEY", "test-key")


def _video_item(video_id="vid1", title="a claude skill walkthrough"):
    return {
        "id": {"videoId": video_id},
        "snippet": {"title": title, "description": "desc"},
    }


def _fake_get(search_items, view_counts):
    def fake_get(url, params=None, timeout=None):  # noqa: ARG001
        resp = MagicMock()
        resp.raise_for_status.return_value = None
        if url == harvest_youtube.SEARCH_URL:
            resp.json.return_value = {"items": search_items}
        elif url == harvest_youtube.VIDEOS_URL:
            resp.json.return_value = {
                "items": [
                    {"id": vid, "statistics": {"viewCount": str(views)}}
                    for vid, views in view_counts.items()
                ]
            }
        return resp
    return fake_get


def test_no_op_without_api_key(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)

    result = harvest_youtube.run(limit=10)

    assert result == {"new": 0, "seen_skipped": 0, "errors": 0}


def test_dedupe_skips_seen_url(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)
    (tmp_path / "seen.txt").write_text("https://www.youtube.com/watch?v=vid1\n")
    fake_get = _fake_get([_video_item()], {"vid1": 5000})

    with patch.object(harvest_youtube.requests, "get", side_effect=fake_get):
        result = harvest_youtube.run(limit=10)

    assert result["new"] == 0
    assert result["seen_skipped"] >= 1


def test_records_new_candidates_and_seen(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)
    fake_get = _fake_get([_video_item()], {"vid1": 5000})

    with patch.object(harvest_youtube.requests, "get", side_effect=fake_get):
        result = harvest_youtube.run(limit=10)

    assert result["new"] == 1
    assert "https://www.youtube.com/watch?v=vid1" in (tmp_path / "seen.txt").read_text()


def test_views_below_threshold_is_skipped(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)
    fake_get = _fake_get([_video_item()], {"vid1": 10})

    with patch.object(harvest_youtube.requests, "get", side_effect=fake_get):
        result = harvest_youtube.run(limit=10)

    assert result["new"] == 0


def test_api_failure_increments_errors_not_raises(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)

    with patch.object(harvest_youtube.requests, "get",
                       side_effect=harvest_youtube.requests.RequestException("boom")):
        result = harvest_youtube.run(limit=10)

    assert result["errors"] == len(harvest_youtube.KEYWORDS)
    assert result["new"] == 0
