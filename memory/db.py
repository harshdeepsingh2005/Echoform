"""
db.py

Low-level database utilities for ECHOFORM.
Handles SQLite connections, database initialization, and schema loading.
"""

import sqlite3
from pathlib import Path
from typing import Optional

from config import DB_PATH, BASE_DIR, is_debug


SCHEMA_FILE = BASE_DIR / "memory" / "schema.sql"


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Create and return a SQLite connection.

    Args:
        db_path: Custom database path (optional). Defaults to config.DB_PATH.

    Returns:
        sqlite3.Connection
    """
    path = db_path or str(DB_PATH)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  # dict-like row access
    return conn


def initialize_database() -> None:
    """
    Create database file and load schema if DB does not exist.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    first_time = not DB_PATH.exists()

    conn = get_connection()
    cursor = conn.cursor()

    if first_time:
        if is_debug():
            print("[DB] Initializing new database from schema...")

        _load_schema(cursor)

    conn.commit()
    conn.close()

    if is_debug():
        print(f"[DB] Database ready at: {DB_PATH}")


def _load_schema(cursor: sqlite3.Cursor) -> None:
    """
    Load SQL schema into database.
    """
    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_FILE}")

    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)

    if is_debug():
        print("[DB] Schema loaded successfully.")


def clear_database() -> None:
    """
    DANGER ZONE: Delete DB file (for fresh experiments).
    """
    if DB_PATH.exists():
        DB_PATH.unlink()
        if is_debug():
            print("[DB] Database wiped.")
