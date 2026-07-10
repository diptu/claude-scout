"""TikTok discovery source. Duplicates harvest_github's fetch/parse pattern
on purpose (see harvest_reddit.py's docstring for why); only the flat-file
bookkeeping tail is shared, via harvest_common.py.

TikTok has no public keyword-search API — only the gated Research API
(client_credentials OAuth, application review required). Uses `requests`
directly (no SDK dependency); degrades to a no-op without
TIKTOK_CLIENT_KEY/TIKTOK_CLIENT_SECRET, same as harvest_reddit.py without
praw credentials — in practice most installs won't have Research API access
approved, same realistic outcome as any other unconfigured source here."""
import datetime
import os

import requests

from scout.core.config import PROJECT_ROOT, load_config
from scout.services import harvest_common

CANDIDATES_DIR = PROJECT_ROOT / "candidates"
SEEN_FILE = CANDIDATES_DIR / "seen.txt"
LIBRARY_DIR = PROJECT_ROOT / "library"

KEYWORDS = ["claude skill", "claude code agent", "mcp server"]
# This is the OAuth token *endpoint* URL, not a credential.
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"  # nosec B105
QUERY_URL = "https://open.tiktokapis.com/v2/research/video/query/"
VIDEO_FIELDS = "id,video_description,create_time,view_count,like_count,username"
MIN_VIEWS = 1000
MAX_AGE_DAYS = 30
MAX_COUNT_PER_QUERY = 25


def _credentials() -> tuple[str, str] | None:
    client_key = os.environ.get("TIKTOK_CLIENT_KEY")
    client_secret = os.environ.get("TIKTOK_CLIENT_SECRET")
    if not client_key or not client_secret:
        return None
    return client_key, client_secret


def _access_token(client_key: str, client_secret: str) -> str | None:
    resp = requests.post(
        TOKEN_URL,
        data={
            "client_key": client_key,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json().get("access_token")


def run(limit=None) -> dict:
    credentials = _credentials()
    if credentials is None:
        # Degrades gracefully: no Research API credentials configured.
        return {"new": 0, "seen_skipped": 0, "errors": 0}

    cfg = load_config().get("tiktok", {})
    min_views = cfg.get("min_views", MIN_VIEWS)
    max_age_days = cfg.get("max_age_days", MAX_AGE_DAYS)
    keywords = cfg.get("keywords", KEYWORDS)

    seen = harvest_common.load_seen(SEEN_FILE) | harvest_common.library_urls(LIBRARY_DIR)
    new_urls: list[str] = []
    new_candidates: list[dict] = []
    errors = 0
    seen_skipped = 0

    try:
        token = _access_token(*credentials)
    except requests.RequestException:
        return {"new": 0, "seen_skipped": 0, "errors": 1}
    if not token:
        return {"new": 0, "seen_skipped": 0, "errors": 1}

    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=max_age_days)).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    for keyword in keywords:
        try:
            resp = requests.post(
                QUERY_URL,
                params={"fields": VIDEO_FIELDS},
                json={
                    "query": {
                        "and": [
                            {"operation": "IN", "field_name": "keyword", "field_values": [keyword]},
                        ],
                    },
                    "start_date": start_date,
                    "end_date": end_date,
                    "max_count": MAX_COUNT_PER_QUERY,
                },
                headers=headers,
                timeout=15,
            )
            resp.raise_for_status()
        except requests.RequestException:
            errors += 1
            continue

        videos = resp.json().get("data", {}).get("videos", [])
        for video in videos:
            if limit is not None and len(new_candidates) >= limit:
                break
            views = video.get("view_count", 0)
            if views < min_views:
                continue
            username = video.get("username", "")
            video_id = video.get("id", "")
            url = f"https://www.tiktok.com/@{username}/video/{video_id}"
            if url in seen or url in new_urls:
                seen_skipped += 1
                continue
            description = video.get("video_description", "")
            new_candidates.append({
                "source": "tiktok",
                "name": description[:80] or f"tiktok-{video_id}",
                "url": url,
                "description": description[:300],
                "stars": views,
                "discovered_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            })
            new_urls.append(url)

        if limit is not None and len(new_candidates) >= limit:
            break

    harvest_common.write_candidates(CANDIDATES_DIR, SEEN_FILE, new_candidates, new_urls)

    return {"new": len(new_candidates), "seen_skipped": seen_skipped, "errors": errors}
