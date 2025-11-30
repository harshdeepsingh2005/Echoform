"""
config.py

Central configuration for ECHOFORM.
Includes runtime flags, memory configuration, mutation logic,
Gemini ADK settings, and deployment toggles.
"""

import os
from pathlib import Path

# -----------------------------------------------------------------------------
# PATH CONFIG
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "memory" / "echoform.db"

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE_PATH = LOGS_DIR / "app.log"

# -----------------------------------------------------------------------------
# RUNTIME FLAGS
# -----------------------------------------------------------------------------

DEBUG = True
LOG_TO_CONSOLE = True

MAX_CONTEXT_MESSAGES = 10
MAX_REASONING_LENGTH = 6000
MAX_COMPRESSION_LENGTH = 1500

# -----------------------------------------------------------------------------
# SCORING SYSTEM
# -----------------------------------------------------------------------------

EVALUATION_WEIGHTS = {
    "accuracy": 0.35,
    "clarity": 0.25,
    "depth": 0.20,
    "originality": 0.20,
}

SCORING_THRESHOLDS = {
    "high_score": 0.80,
    "medium_score": 0.60,
    "low_score": 0.40,
}

# -----------------------------------------------------------------------------
# MUTATION ENGINE
# -----------------------------------------------------------------------------

DEFAULT_TRAITS = {
    "creativity": 0.5,
    "formality": 0.5,
    "abstraction": 0.5,
    "verbosity": 0.5,
}

MUTATION_DELTAS = {
    "creativity_up": 0.10,
    "creativity_down": -0.10,
    "abstraction_up": 0.10,
    "abstraction_down": -0.10,
    "verbosity_up": 0.10,
    "verbosity_down": -0.10,
    "formality_up": 0.05,
    "formality_down": -0.05,
}

TRAIT_MIN = 0.0
TRAIT_MAX = 1.0

# -----------------------------------------------------------------------------
# UI LABELS
# -----------------------------------------------------------------------------

APP_NAME = "ECHOFORM"
APP_TAGLINE = (
    "A self-reflecting cognitive system powered by multi-agent intelligence "
    "and Google Gemini ADK."
)

SHOW_INTERNALS_IN_UI = True

# -----------------------------------------------------------------------------
# GOOGLE GEMINI ADK CONFIGURATION
# -----------------------------------------------------------------------------

# Ensure you set:
# export GEMINI_API_KEY="your_key_here"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Default model (safe & fast)
DEFAULT_GEMINI_MODEL = "models/gemini-2.5-flash"

# Retry policy
GEMINI_MAX_RETRIES = 2
GEMINI_STREAMING_ENABLED = False

# -----------------------------------------------------------------------------
# SYSTEM HELPERS
# -----------------------------------------------------------------------------

def ensure_directories() -> None:
    """Ensure memory & logs exist."""
    (BASE_DIR / "memory").mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def is_debug() -> bool:
    return DEBUG


def gemini_enabled() -> bool:
    return bool(GEMINI_API_KEY)


def get_database_uri() -> str:
    return str(DB_PATH)
