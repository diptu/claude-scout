from unittest.mock import MagicMock, patch

from scout.services import harvest_twitter


def _patch_dirs(monkeypatch, tmp_path):
    monkeypatch.setattr(harvest_twitter, "CANDIDATES_DIR", tmp_path)
    monkeypatch.setattr(harvest_twitter, "SEEN_FILE", tmp_path / "seen.txt")
    monkeypatch.setattr(harvest_twitter, "LIBRARY_DIR", tmp_path / "library")
    monkeypatch.setattr(harvest_twitter, "load_config", lambda: {})
    monkeypatch.setenv("TWITTER_BEARER_TOKEN", "test-token")


def _mock_response(tweets):
    resp = MagicMock()
    resp.json.return_value = {"data": tweets}
    resp.raise_for_status.return_value = None
    return resp


def _tweet(tweet_id="1", text="check out this claude skill", likes=40, retweets=20):
    return {
        "id": tweet_id,
        "text": text,
        "public_metrics": {"like_count": likes, "retweet_count": retweets},
    }


def test_no_op_without_bearer_token(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)
    monkeypatch.delenv("TWITTER_BEARER_TOKEN", raising=False)

    result = harvest_twitter.run(limit=10)

    assert result == {"new": 0, "seen_skipped": 0, "errors": 0}


def test_dedupe_skips_seen_url(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)
    (tmp_path / "seen.txt").write_text("https://twitter.com/i/web/status/1\n")

    with patch.object(harvest_twitter.requests, "get", return_value=_mock_response([_tweet()])):
        result = harvest_twitter.run(limit=10)

    assert result["new"] == 0
    assert result["seen_skipped"] >= 1


def test_records_new_candidates_and_seen(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)

    with patch.object(harvest_twitter.requests, "get", return_value=_mock_response([_tweet()])):
        result = harvest_twitter.run(limit=10)

    assert result["new"] == 1
    assert "https://twitter.com/i/web/status/1" in (tmp_path / "seen.txt").read_text()


def test_engagement_below_threshold_is_skipped(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)
    low_engagement = _tweet(likes=1, retweets=0)

    with patch.object(harvest_twitter.requests, "get",
                       return_value=_mock_response([low_engagement])):
        result = harvest_twitter.run(limit=10)

    assert result["new"] == 0


def test_api_failure_increments_errors_not_raises(tmp_path, monkeypatch):
    _patch_dirs(monkeypatch, tmp_path)

    with patch.object(harvest_twitter.requests, "get",
                       side_effect=harvest_twitter.requests.RequestException("boom")):
        result = harvest_twitter.run(limit=10)

    assert result["errors"] == len(harvest_twitter.KEYWORDS)
    assert result["new"] == 0
