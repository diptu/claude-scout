"""YouTube discovery source. Duplicates harvest_github's fetch/parse pattern
on purpose (see harvest_reddit.py's docstring for why); only the flat-file
bookkeeping tail is shared, via harvest_common.py.

Uses the YouTube Data API v3 directly with `requests` (no SDK dependency) —
an API key is required. Degrades to a no-op without one, same as
harvest_reddit.py without praw credentials. Two calls per keyword: search
for matching videos, then videos.list for the view counts search doesn't
return, so results can be filtered by min_views like the other sources'
engagement thresholds."""
import datetime
import os

import requests

from scout.core.config import PROJECT_ROOT, load_config
from scout.services import harvest_common

CANDIDATES_DIR = PROJECT_ROOT / "candidates"
SEEN_FILE = CANDIDATES_DIR / "seen.txt"
LIBRARY_DIR = PROJECT_ROOT / "library"

KEYWORDS = ["claude skill", "claude code agent", "mcp server"]
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
MIN_VIEWS = 1000
MAX_AGE_DAYS = 180
MAX_RESULTS_PER_QUERY = 25


def _api_key() -> str | None:
    return os.environ.get("YOUTUBE_API_KEY")


def _fetch_statistics(video_ids: list, api_key: str) -> dict:
    if not video_ids:
        return {}
    resp = requests.get(
        VIDEOS_URL,
        params={"part": "statistics", "id": ",".join(video_ids), "key": api_key},
        timeout=15,
    )
    resp.raise_for_status()
    return {
        item["id"]: int(item.get("statistics", {}).get("viewCount", 0))
        for item in resp.json().get("items", [])
    }


def run(limit=None) -> dict:
    api_key = _api_key()
    if not api_key:
        # Degrades gracefully: no API key configured.
        return {"new": 0, "seen_skipped": 0, "errors": 0}

    cfg = load_config().get("youtube", {})
    min_views = cfg.get("min_views", MIN_VIEWS)
    max_age_days = cfg.get("max_age_days", MAX_AGE_DAYS)
    keywords = cfg.get("keywords", KEYWORDS)

    seen = harvest_common.load_seen(SEEN_FILE) | harvest_common.library_urls(LIBRARY_DIR)
    new_urls: list[str] = []
    new_candidates: list[dict] = []
    errors = 0
    seen_skipped = 0

    published_after = (
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=max_age_days)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    for keyword in keywords:
        try:
            resp = requests.get(
                SEARCH_URL,
                params={
                    "part": "snippet",
                    "q": keyword,
                    "type": "video",
                    "order": "date",
                    "publishedAfter": published_after,
                    "maxResults": MAX_RESULTS_PER_QUERY,
                    "key": api_key,
                },
                timeout=15,
            )
            resp.raise_for_status()
            items = resp.json().get("items", [])
            video_ids = [item["id"]["videoId"] for item in items]
            view_counts = _fetch_statistics(video_ids, api_key)
        except requests.RequestException:
            errors += 1
            continue

        for item in items:
            if limit is not None and len(new_candidates) >= limit:
                break
            video_id = item["id"]["videoId"]
            views = view_counts.get(video_id, 0)
            if views < min_views:
                continue
            url = f"https://www.youtube.com/watch?v={video_id}"
            if url in seen or url in new_urls:
                seen_skipped += 1
                continue
            snippet = item.get("snippet", {})
            new_candidates.append({
                "source": "youtube",
                "name": snippet.get("title", "")[:80],
                "url": url,
                "description": snippet.get("description", "")[:300],
                "stars": views,
                "discovered_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            })
            new_urls.append(url)

        if limit is not None and len(new_candidates) >= limit:
            break

    harvest_common.write_candidates(CANDIDATES_DIR, SEEN_FILE, new_candidates, new_urls)

    return {"new": len(new_candidates), "seen_skipped": seen_skipped, "errors": errors}
