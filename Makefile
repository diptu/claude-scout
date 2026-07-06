SRC := src/main.py
PYTHON := python3

.PHONY: help install install-dev lint test check \
        harvest build eval scout search show review clean

help:
	@echo "claude-scout — available targets:"
	@echo "  make install       install runtime dependencies"
	@echo "  make install-dev   install runtime + dev dependencies (pytest, ruff)"
	@echo "  make lint          run ruff"
	@echo "  make test          run pytest"
	@echo "  make check         lint + test (what CI runs)"
	@echo "  make harvest       run --mode harvest (add LIMIT=N, GITHUB_ONLY=1 to scope it)"
	@echo "  make build         run --mode build (add LIMIT=N)"
	@echo "  make eval          run --mode eval"
	@echo "  make scout         run --mode scout (harvest + build + eval)"
	@echo "  make search KEYWORD=git   run --mode search"
	@echo "  make show NAME=git-commit-craft   run --mode show"
	@echo "  make review        run --mode review (interactive)"
	@echo "  make clean         remove __pycache__/.pytest_cache"

install:
	$(PYTHON) -m pip install -r requirements.txt

install-dev: install
	$(PYTHON) -m pip install pytest ruff

lint:
	$(PYTHON) -m ruff check .

test:
	$(PYTHON) -m pytest tests/ -v

check: lint test

LIMIT_FLAG := $(if $(LIMIT),--limit $(LIMIT),)
GITHUB_ONLY_FLAG := $(if $(GITHUB_ONLY),--github-only,)

harvest:
	$(PYTHON) $(SRC) --mode harvest $(LIMIT_FLAG) $(GITHUB_ONLY_FLAG)

build:
	$(PYTHON) $(SRC) --mode build $(LIMIT_FLAG)

eval:
	$(PYTHON) $(SRC) --mode eval

scout:
	$(PYTHON) $(SRC) --mode scout $(LIMIT_FLAG)

search:
	$(PYTHON) $(SRC) --mode search $(KEYWORD)

show:
	$(PYTHON) $(SRC) --mode show $(NAME)

review:
	$(PYTHON) $(SRC) --mode review

clean:
	find . -type d -name "__pycache__" -not -path "./.git/*" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache
