import json

from scout.services import harvest_common


def test_load_seen_missing_file_returns_empty_set(tmp_path):
    assert harvest_common.load_seen(tmp_path / "seen.txt") == set()


def test_load_seen_reads_lines(tmp_path):
    seen_file = tmp_path / "seen.txt"
    seen_file.write_text("https://a\nhttps://b\n")
    assert harvest_common.load_seen(seen_file) == {"https://a", "https://b"}


def test_library_urls_missing_dir_returns_empty_set(tmp_path):
    assert harvest_common.library_urls(tmp_path / "library") == set()


def test_library_urls_reads_source_url_from_meta(tmp_path):
    library_dir = tmp_path / "library"
    entry = library_dir / "skill-a"
    entry.mkdir(parents=True)
    (entry / "meta.json").write_text(json.dumps({"source_url": "https://x/skill-a"}))

    assert harvest_common.library_urls(library_dir) == {"https://x/skill-a"}


def test_append_seen_appends_to_existing_file(tmp_path):
    seen_file = tmp_path / "seen.txt"
    seen_file.write_text("https://a\n")
    harvest_common.append_seen(seen_file, ["https://b", "https://c"])
    assert seen_file.read_text().splitlines() == ["https://a", "https://b", "https://c"]


def test_write_candidates_noop_when_empty(tmp_path):
    harvest_common.write_candidates(tmp_path, tmp_path / "seen.txt", [], [])
    assert not (tmp_path / "seen.txt").exists()
    assert list(tmp_path.glob("discovery-*.json")) == []


def test_write_candidates_writes_discovery_file_and_seen(tmp_path):
    seen_file = tmp_path / "seen.txt"
    candidates = [{"source": "x", "name": "n", "url": "https://x/n"}]
    harvest_common.write_candidates(tmp_path, seen_file, candidates, ["https://x/n"])

    discovery_files = list(tmp_path.glob("discovery-*.json"))
    assert len(discovery_files) == 1
    assert json.loads(discovery_files[0].read_text()) == candidates
    assert "https://x/n" in seen_file.read_text()
