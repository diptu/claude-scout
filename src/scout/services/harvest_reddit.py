"""Reddit discovery source (Phase 6). Deliberately duplicates
harvest_github's fetch/parse pattern rather than sharing an abstraction for
that part — see architecture.md's "no BaseScraper" decision. The flat-file
bookkeeping tail (seen.txt, discovery-<date>.json) is shared via
harvest_common.py; that part earned de-duplication once a third+ source
needed the identical code (CLAUDE.md principle 2)."""
import datetime
import os

from scout.core.config import PROJECT_ROOT, load_config
from scout.services import harvest_common

CANDIDATES_DIR = PROJECT_ROOT / "candidates"
SEEN_FILE = CANDIDATES_DIR / "seen.txt"
LIBRARY_DIR = PROJECT_ROOT / "library"

SUBREDDITS = ["ClaudeAI", "LocalLLaMA", "Anthropic"]
KEYWORDS = ["claude skill", "claude code agent", "mcp server"]
MIN_SCORE = 50
MIN_COMMENTS = 10
MAX_AGE_DAYS = 7


def _get_reddit():
    try:
        # Lazy on purpose: praw is optional and this source degrades to a
        # no-op without it.
        import praw  # pylint: disable=import-outside-toplevel
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

    cfg = load_config().get("reddit", {})
    min_score = cfg.get("min_score", MIN_SCORE)
    min_comments = cfg.get("min_comments", MIN_COMMENTS)
    max_age_days = cfg.get("max_age_days", MAX_AGE_DAYS)
    subreddits = cfg.get("subreddits", SUBREDDITS)
    keywords = cfg.get("keywords", KEYWORDS)

    seen = harvest_common.load_seen(SEEN_FILE) | harvest_common.library_urls(LIBRARY_DIR)
    new_urls: list[str] = []
    new_candidates: list[dict] = []
    errors = 0
    seen_skipped = 0
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=max_age_days)

    for sub_name in subreddits:
        try:
            subreddit = reddit.subreddit(sub_name)
            for post in subreddit.new(limit=50):
                if limit is not None and len(new_candidates) >= limit:
                    break
                posted_at = datetime.datetime.fromtimestamp(
                    post.created_utc, tz=datetime.timezone.utc
                )
                if posted_at < cutoff:
                    continue
                if post.score <= min_score or post.num_comments <= min_comments:
                    continue
                text = f"{post.title} {post.selftext}".lower()
                if not any(k in text for k in keywords):
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
        except Exception:  # pylint: disable=broad-exception-caught
            # praw raises assorted exception types; one bad subreddit must
            # not abort the others, so count it and move on.
            errors += 1
            continue

        if limit is not None and len(new_candidates) >= limit:
            break

    harvest_common.write_candidates(CANDIDATES_DIR, SEEN_FILE, new_candidates, new_urls)

    return {"new": len(new_candidates), "seen_skipped": seen_skipped, "errors": errors}
