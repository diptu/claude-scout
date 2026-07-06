"""Project paths and user-editable configuration (defaults/config.yml)."""
from pathlib import Path

import yaml

# src/scout/core/config.py -> parents[3] = repo root (src/scout/core -> scout -> src -> root).
# Centralized here (rather than recomputed per module) since every module
# needs it and the src/ layout means it's no longer a trivial one-liner.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONFIG_FILE = PROJECT_ROOT / "defaults" / "config.yml"


def load_config() -> dict:
    """Candidacy criteria from defaults/config.yml; {} if absent so callers
    fall back to their built-in defaults."""
    if not CONFIG_FILE.exists():
        return {}
    with CONFIG_FILE.open() as f:
        return yaml.safe_load(f) or {}
