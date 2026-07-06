"""GitHub discovery source. See backend_service_specs/harvest_github.md."""
import datetime
import os
import time

import requests

from scout.util import PROJECT_ROOT, read_json, write_json

CANDIDATES_DIR = PROJECT_ROOT / "candidates"
SEEN_FILE = CANDIDATES_DIR / "seen.txt"

KEYWORDS = ["claude skill", "claude code agent", "mcp server"]
API_URL = "https://api.github.com/search/repositories"
RATE_LIMIT_SLEEP_THRESHOLD = 5
MIN_STARS = 50
MAX_AGE_DAYS = 180


def _load_seen() -> set:
    if not SEEN_FILE.exists():
        return set()
    return set(SEEN_FILE.read_text().splitlines())


def _append_seen(urls) -> None:
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SEEN_FILE.open("a") as f:
        for url in urls:
            f.write(url + "\n")


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
    seen = _load_seen()
    new_urls = []
    new_candidates = []
    errors = 0
    seen_skipped = 0

    since = (datetime.date.today() - datetime.timedelta(days=MAX_AGE_DAYS)).isoformat()

    for keyword in KEYWORDS:
        query = f"{keyword} in:name,description stars:>={MIN_STARS} pushed:>={since}"
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

    if new_candidates:
        today_file = CANDIDATES_DIR / f"discovery-{datetime.date.today().isoformat()}.json"
        existing = read_json(today_file, default=[])
        write_json(today_file, existing + new_candidates)
        _append_seen(new_urls)

    return {"new": len(new_candidates), "seen_skipped": seen_skipped, "errors": errors}
