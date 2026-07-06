"""Reddit discovery source (Phase 6). Deliberately duplicates
harvest_github's pattern rather than sharing an abstraction — see
architecture.md's "no BaseScraper" decision."""
import datetime
import os

from scout.util import PROJECT_ROOT, read_json, write_json

CANDIDATES_DIR = PROJECT_ROOT / "candidates"
SEEN_FILE = CANDIDATES_DIR / "seen.txt"

SUBREDDITS = ["ClaudeAI", "LocalLLaMA", "Anthropic"]
KEYWORDS = ["claude skill", "claude code agent", "mcp server"]
MIN_SCORE = 50
MIN_COMMENTS = 10
MAX_AGE_DAYS = 7


def _load_seen() -> set:
    if not SEEN_FILE.exists():
        return set()
    return set(SEEN_FILE.read_text().splitlines())


def _append_seen(urls) -> None:
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SEEN_FILE.open("a") as f:
        for url in urls:
            f.write(url + "\n")


def _get_reddit():
    try:
        import praw
    except ImportError:
        return None
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    if not client_id or not client_secret:
        return None
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="claude-scout/0.1",
    )


def run(limit=None) -> dict:
    reddit = _get_reddit()
    if reddit is None:
        # Degrades gracefully: no praw installed or no credentials configured.
        return {"new": 0, "seen_skipped": 0, "errors": 0}

    seen = _load_seen()
    new_urls = []
    new_candidates = []
    errors = 0
    seen_skipped = 0
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=MAX_AGE_DAYS)

    for sub_name in SUBREDDITS:
        try:
            subreddit = reddit.subreddit(sub_name)
            for post in subreddit.new(limit=50):
                if limit is not None and len(new_candidates) >= limit:
                    break
                posted_at = datetime.datetime.utcfromtimestamp(post.created_utc)
                if posted_at < cutoff:
                    continue
                if post.score <= MIN_SCORE or post.num_comments <= MIN_COMMENTS:
                    continue
                text = f"{post.title} {post.selftext}".lower()
                if not any(k in text for k in KEYWORDS):
                    continue
                url = f"https://reddit.com{post.permalink}"
                if url in seen or url in new_urls:
                    seen_skipped += 1
                    continue
                new_candidates.append({
                    "source": "reddit",
                    "name": post.title[:80],
                    "url": url,
                    "description": post.selftext[:300],
                    "stars": post.score,
                    "discovered_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                })
                new_urls.append(url)
        except Exception:
            errors += 1
            continue

        if limit is not None and len(new_candidates) >= limit:
            break

    if new_candidates:
        today_file = CANDIDATES_DIR / f"discovery-{datetime.date.today().isoformat()}.json"
        existing = read_json(today_file, default=[])
        write_json(today_file, existing + new_candidates)
        _append_seen(new_urls)

    return {"new": len(new_candidates), "seen_skipped": seen_skipped, "errors": errors}
