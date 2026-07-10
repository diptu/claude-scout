PYTHON := python3
export PYTHONPATH := src

.PHONY: help install install-dev lint mypy pylint bandit test check \
        harvest reset-harvest build eval committee backfill insights digest scout search show review clean

help:
	@echo "claude-scout — available targets:"
	@echo "  make install       install runtime dependencies"
	@echo "  make install-dev   install runtime + dev dependencies (pytest, ruff)"
	@echo "  make lint          run ruff"
	@echo "  make mypy          run mypy type checks"
	@echo "  make pylint        run pylint"
	@echo "  make bandit        run bandit security checks"
	@echo "  make test          run pytest"
	@echo "  make check         lint + mypy + pylint + bandit + test (what CI runs)"
	@echo "  make harvest       pulls candidates into candidates/, deduped via seen.txt (add LIMIT=N, GITHUB_ONLY=1 to scope to just GitHub)"
	@echo "                     GitHub works out of the box; Reddit/X/YouTube/TikTok need credentials or no-op:"
	@echo "                       Reddit    REDDIT_CLIENT_ID + REDDIT_CLIENT_SECRET"
	@echo "                       X/Twitter TWITTER_BEARER_TOKEN"
	@echo "                       YouTube   YOUTUBE_API_KEY"
	@echo "                       TikTok    TIKTOK_CLIENT_KEY + TIKTOK_CLIENT_SECRET (Research API, needs approval)"
	@echo "  make reset-harvest wipe candidates/discovery-*.json + seen.txt (interactive confirm)"
	@echo "  make build         claude CLI drafts a SKILL.md per candidate into drafts/<name>/, treating candidate content as untrusted"
	@echo "  make eval          runs a test battery per draft via claude; pass/fail is exit-code/timeout only, never quality"
	@echo "  make committee     five exec personas score each eval-passed draft 1-5; below threshold -> trash/, hired drafts move to the council stage"
	@echo "                     council stage: five-advisor-plus-chairman panel checks hired drafts for redundancy against library/ (no separate target — runs inside make committee)"
	@echo "  make backfill      one-off: score existing library/ entries lacking a committee_score"
	@echo "  make insights      run --mode insights (aggregate existing committee/council verdict JSON)"
	@echo "  make digest        run --mode digest (ranked top-10 report of library/ skills)"
	@echo "  make scout         run --mode scout (harvest + build + eval + committee)"
	@echo "  make search KEYWORD=git   run --mode search"
	@echo "  make show NAME=git-commit-craft   run --mode show"
	@echo "  make review        run --mode review (interactive)"
	@echo "  make clean         remove __pycache__/.pytest_cache"

install:
	$(PYTHON) -m pip install -e .

install-dev: install
	$(PYTHON) -m pip install pytest ruff mypy pylint bandit types-pyyaml

lint:
	$(PYTHON) -m ruff check .

mypy:
	$(PYTHON) -m mypy

pylint:
	$(PYTHON) -m pylint src tests

bandit:
	$(PYTHON) -m bandit -r src -q

test:
	$(PYTHON) -m pytest tests/ -v

check: lint mypy pylint bandit test

LIMIT_FLAG := $(if $(LIMIT),--limit $(LIMIT),)
GITHUB_ONLY_FLAG := $(if $(GITHUB_ONLY),--github-only,)

harvest:
	$(PYTHON) -m scout --mode harvest $(LIMIT_FLAG) $(GITHUB_ONLY_FLAG)

reset-harvest:
	$(PYTHON) -m scout --mode reset-harvest

build:
	$(PYTHON) -m scout --mode build $(LIMIT_FLAG)

eval:
	$(PYTHON) -m scout --mode eval

committee:
	$(PYTHON) -m scout --mode committee

backfill:
	$(PYTHON) scripts/backfill_committee.py

insights:
	$(PYTHON) -m scout --mode insights

digest:
	$(PYTHON) -m scout --mode digest

scout:
	$(PYTHON) -m scout --mode scout $(LIMIT_FLAG)

search:
	$(PYTHON) -m scout --mode search $(KEYWORD)

show:
	$(PYTHON) -m scout --mode show $(NAME)

review:
	$(PYTHON) -m scout --mode review

clean:
	find . -type d -name "__pycache__" -not -path "./.git/*" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache
