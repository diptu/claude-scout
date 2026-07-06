from scout.commands import reset_harvest


def _patch_dirs(monkeypatch, candidates_dir):
    monkeypatch.setattr(reset_harvest, "CANDIDATES_DIR", candidates_dir)
    monkeypatch.setattr(reset_harvest, "SEEN_FILE", candidates_dir / "seen.txt")


def test_nothing_to_reset(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    _patch_dirs(monkeypatch, candidates_dir)

    result = reset_harvest.run(confirm=lambda _: "y")

    assert result == {"discovery_files_removed": 0, "seen_removed": False}


def test_declining_confirmation_leaves_files_intact(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    (candidates_dir / "discovery-2026-07-06.json").write_text("[]")
    (candidates_dir / "seen.txt").write_text("https://x/repo\n")
    _patch_dirs(monkeypatch, candidates_dir)

    result = reset_harvest.run(confirm=lambda _: "n")

    assert result == {"discovery_files_removed": 0, "seen_removed": False}
    assert (candidates_dir / "discovery-2026-07-06.json").exists()
    assert (candidates_dir / "seen.txt").exists()


def test_confirming_removes_discovery_files_and_seen(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    (candidates_dir / "discovery-2026-07-05.json").write_text("[]")
    (candidates_dir / "discovery-2026-07-06.json").write_text("[]")
    (candidates_dir / "seen.txt").write_text("https://x/repo\n")
    _patch_dirs(monkeypatch, candidates_dir)

    result = reset_harvest.run(confirm=lambda _: "y")

    assert result == {"discovery_files_removed": 2, "seen_removed": True}
    assert list(candidates_dir.glob("discovery-*.json")) == []
    assert not (candidates_dir / "seen.txt").exists()


def test_seen_only_without_discovery_files(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    (candidates_dir / "seen.txt").write_text("https://x/repo\n")
    _patch_dirs(monkeypatch, candidates_dir)

    result = reset_harvest.run(confirm=lambda _: "y")

    assert result == {"discovery_files_removed": 0, "seen_removed": True}
    assert not (candidates_dir / "seen.txt").exists()
