"""
repository.py

High-level abstraction for ECHOFORM's cognitive memory.
Provides safe, semantic functions instead of raw SQL.
"""

import json
import uuid
from typing import Dict, List, Any, Optional

from memory.db import get_connection
from config import MAX_CONTEXT_MESSAGES, DEFAULT_TRAITS


# ==========================================================
# SESSION CONTROL
# ==========================================================

def create_session() -> str:
    """
    Create a new cognitive session and return session_uuid.
    """
    session_uuid = str(uuid.uuid4())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sessions (session_uuid)
        VALUES (?)
    """, (session_uuid,))

    # Initialize traits
    _initialize_traits(cursor, session_uuid)

    conn.commit()
    conn.close()

    return session_uuid


def _initialize_traits(cursor, session_uuid: str):
    """
    Insert default trait profile.
    """
    cursor.execute("""
        INSERT INTO session_traits (session_uuid, creativity, abstraction, verbosity, formality)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session_uuid,
        DEFAULT_TRAITS["creativity"],
        DEFAULT_TRAITS["abstraction"],
        DEFAULT_TRAITS["verbosity"],
        DEFAULT_TRAITS["formality"],
    ))


# ==========================================================
# MESSAGE STORAGE
# ==========================================================

def save_message(session_uuid: str, role: str, content: str) -> None:
    """
    Save a message in memory.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (session_uuid, role, content)
        VALUES (?, ?, ?)
    """, (session_uuid, role, content))

    conn.commit()
    conn.close()


def get_recent_context(session_uuid: str, limit: int = MAX_CONTEXT_MESSAGES) -> List[Dict]:
    """
    Load recent conversation context.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content
        FROM messages
        WHERE session_uuid = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (session_uuid, limit))

    rows = cursor.fetchall()
    conn.close()

    # reverse to chronological
    return [dict(row) for row in reversed(rows)]


# ==========================================================
# REASONING STORAGE
# ==========================================================

def save_reasoning_snapshot(
    session_uuid: str,
    raw_reasoning: str,
    compressed: str,
    traits: Dict[str, Any]
) -> None:
    """
    Store internal cognition.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reasoning_snapshots
        (session_uuid, raw_reasoning, compressed_reasoning, traits_json)
        VALUES (?, ?, ?, ?)
    """, (
        session_uuid,
        raw_reasoning,
        compressed,
        json.dumps(traits)
    ))

    conn.commit()
    conn.close()


# ==========================================================
# EVALUATION STORAGE
# ==========================================================

def save_evaluation(
    session_uuid: str,
    scores: Dict[str, float]
) -> None:
    """
    Persist evaluation scores.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO evaluations
        (session_uuid, accuracy, clarity, depth, originality, overall)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session_uuid,
        scores["accuracy"],
        scores["clarity"],
        scores["depth"],
        scores["originality"],
        scores["overall"],
    ))

    conn.commit()
    conn.close()


# ==========================================================
# TRAIT MANAGEMENT
# ==========================================================

def get_traits(session_uuid: str) -> Dict[str, float]:
    """
    Load personality vector.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT creativity, abstraction, verbosity, formality
        FROM session_traits
        WHERE session_uuid = ?
    """, (session_uuid,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise ValueError("Session not found when loading traits.")

    return dict(row)


def update_traits(session_uuid: str, new_traits: Dict[str, float]) -> None:
    """
    Update personality profile after mutation.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE session_traits
        SET creativity = ?, abstraction = ?, verbosity = ?, formality = ?,
            last_mutation = CURRENT_TIMESTAMP
        WHERE session_uuid = ?
    """, (
        new_traits["creativity"],
        new_traits["abstraction"],
        new_traits["verbosity"],
        new_traits["formality"],
        session_uuid,
    ))

    conn.commit()
    conn.close()


# ==========================================================
# SESSION METADATA
# ==========================================================

def increment_mutation_level(session_uuid: str) -> None:
    """
    Increase mutation counter.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE sessions
        SET mutation_level = mutation_level + 1,
            updated_at = CURRENT_TIMESTAMP
        WHERE session_uuid = ?
    """, (session_uuid,))

    conn.commit()
    conn.close()


def get_mutation_level(session_uuid: str) -> int:
    """
    Return current mutation level.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mutation_level FROM sessions WHERE session_uuid = ?
    """, (session_uuid,))

    row = cursor.fetchone()
    conn.close()

    return int(row["mutation_level"])
