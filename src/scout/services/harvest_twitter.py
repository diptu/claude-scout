"""Twitter/X discovery source. Duplicates harvest_github's fetch/parse
pattern on purpose (see harvest_reddit.py's docstring for why); only the
flat-file bookkeeping tail is shared, via harvest_common.py.

Uses the X API v2 recent-search endpoint directly with `requests` (no SDK
dependency) — a Bearer token is required. Degrades to a no-op without one,
same as harvest_reddit.py without praw credentials."""
import datetime
import os

import requests

from scout.core.config import PROJECT_ROOT, load_config
from scout.services import harvest_common

CANDIDATES_DIR = PROJECT_ROOT / "candidates"
SEEN_FILE = CANDIDATES_DIR / "seen.txt"
LIBRARY_DIR = PROJECT_ROOT / "library"

KEYWORDS = ["claude skill", "claude code agent", "mcp server"]
API_URL = "https://api.twitter.com/2/tweets/search/recent"
MIN_ENGAGEMENT = 50
MAX_AGE_DAYS = 7
# X's recent-search endpoint only covers the last 7 days regardless of
# max_age_days — a longer config value just narrows start_time further
# within that same window.
MAX_RESULTS_PER_QUERY = 50


def _bearer_token() -> str | None:
    return os.environ.get("TWITTER_BEARER_TOKEN")


def run(limit=None) -> dict:
    token = _bearer_token()
    if not token:
        # Degrades gracefully: no bearer token configured.
        return {"new": 0, "seen_skipped": 0, "errors": 0}

    cfg = load_config().get("twitter", {})
    min_engagement = cfg.get("min_engagement", MIN_ENGAGEMENT)
    max_age_days = cfg.get("max_age_days", MAX_AGE_DAYS)
    keywords = cfg.get("keywords", KEYWORDS)

    seen = harvest_common.load_seen(SEEN_FILE) | harvest_common.library_urls(LIBRARY_DIR)
    new_urls: list[str] = []
    new_candidates: list[dict] = []
    errors = 0
    seen_skipped = 0

    start_time = (
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=max_age_days)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    headers = {"Authorization": f"Bearer {token}"}

    for keyword in keywords:
        try:
            resp = requests.get(
                API_URL,
                params={
                    "query": f"{keyword} -is:retweet",
                    "max_results": str(MAX_RESULTS_PER_QUERY),
                    "start_time": start_time,
                    "tweet.fields": "public_metrics,created_at",
                },
                headers=headers,
                timeout=15,
            )
            resp.raise_for_status()
        except requests.RequestException:
            errors += 1
            continue

        for tweet in resp.json().get("data", []):
            if limit is not None and len(new_candidates) >= limit:
                break
            metrics = tweet.get("public_metrics", {})
            engagement = metrics.get("like_count", 0) + metrics.get("retweet_count", 0)
            if engagement < min_engagement:
                continue
            url = f"https://twitter.com/i/web/status/{tweet['id']}"
            if url in seen or url in new_urls:
                seen_skipped += 1
                continue
            text = tweet.get("text", "")
            new_candidates.append({
                "source": "twitter",
                "name": text[:80],
                "url": url,
                "description": text[:300],
                "stars": engagement,
                "discovered_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            })
            new_urls.append(url)

        if limit is not None and len(new_candidates) >= limit:
            break

    harvest_common.write_candidates(CANDIDATES_DIR, SEEN_FILE, new_candidates, new_urls)

    return {"new": len(new_candidates), "seen_skipped": seen_skipped, "errors": errors}
