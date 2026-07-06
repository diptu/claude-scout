from scout.core import logger


def test_log_event_appends_timestamped_line(tmp_path, monkeypatch):
    monkeypatch.setattr(logger, "LOGS_DIR", tmp_path / "logs")

    logger.log_event("harvest", "harvest: 2 new candidates, 0 already seen, 0 errors")
    logger.log_event("harvest", "harvest: 1 new candidates, 2 already seen, 0 errors")

    log_file = tmp_path / "logs" / "harvest.log"
    lines = log_file.read_text().splitlines()

    assert len(lines) == 2
    assert lines[0].endswith("harvest: 2 new candidates, 0 already seen, 0 errors")
    assert lines[1].endswith("harvest: 1 new candidates, 2 already seen, 0 errors")
    # first token on each line should be an ISO-8601 timestamp
    assert "T" in lines[0].split(" ")[0]


def test_log_event_creates_separate_files_per_stage(tmp_path, monkeypatch):
    monkeypatch.setattr(logger, "LOGS_DIR", tmp_path / "logs")

    logger.log_event("build", "build: 1 drafted, 0 failed")
    logger.log_event("eval", "eval: 1 passed, 0 failed")

    assert (tmp_path / "logs" / "build.log").exists()
    assert (tmp_path / "logs" / "eval.log").exists()
