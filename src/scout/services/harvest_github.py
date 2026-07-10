"""GitHub discovery source. See backend_service_specs/harvest_github.md."""
import datetime
import os
import time

import requests

from scout.core.config import PROJECT_ROOT, load_config
from scout.services import harvest_common

CANDIDATES_DIR = PROJECT_ROOT / "candidates"
SEEN_FILE = CANDIDATES_DIR / "seen.txt"
LIBRARY_DIR = PROJECT_ROOT / "library"

KEYWORDS = ["claude skill", "claude code agent", "mcp server"]
API_URL = "https://api.github.com/search/repositories"
RATE_LIMIT_SLEEP_THRESHOLD = 5
MIN_STARS = 50
MAX_AGE_DAYS = 180


def _headers() -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def _respect_rate_limit(response) -> None:
    remaining = response.headers.get("X-RateLimit-Remaining")
    reset = response.headers.get("X-RateLimit-Reset")
    if remaining is not None and int(remaining) < RATE_LIMIT_SLEEP_THRESHOLD and reset:
        sleep_for = max(0, int(reset) - int(time.time())) + 1
        time.sleep(min(sleep_for, 60))


def run(limit=None) -> dict:
    cfg = load_config().get("github", {})
    min_stars = cfg.get("min_stars", MIN_STARS)
    max_age_days = cfg.get("max_age_days", MAX_AGE_DAYS)
    keywords = cfg.get("keywords", KEYWORDS)

    seen = harvest_common.load_seen(SEEN_FILE) | harvest_common.library_urls(LIBRARY_DIR)
    new_urls: list[str] = []
    new_candidates: list[dict] = []
    errors = 0
    seen_skipped = 0

    since = (datetime.date.today() - datetime.timedelta(days=max_age_days)).isoformat()

    for keyword in keywords:
        query = f"{keyword} in:name,description stars:>={min_stars} pushed:>={since}"
        try:
            resp = requests.get(
                API_URL,
                params={"q": query, "sort": "stars", "order": "desc"},
                headers=_headers(),
                timeout=15,
            )
            resp.raise_for_status()
            _respect_rate_limit(resp)
        except requests.RequestException:
            errors += 1
            continue

        for item in resp.json().get("items", []):
            if limit is not None and len(new_candidates) >= limit:
                break
            url = item["html_url"]
            if url in seen or url in new_urls:
                seen_skipped += 1
                continue
            new_candidates.append({
                "source": "github",
                "name": item["full_name"],
                "url": url,
                "description": item.get("description") or "",
                "stars": item.get("stargazers_count", 0),
                "discovered_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            })
            new_urls.append(url)

        if limit is not None and len(new_candidates) >= limit:
            break

    harvest_common.write_candidates(CANDIDATES_DIR, SEEN_FILE, new_candidates, new_urls)

    return {"new": len(new_candidates), "seen_skipped": seen_skipped, "errors": errors}
