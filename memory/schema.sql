-- ==========================================================
-- ECHOFORM - Cognitive Memory Schema
-- Database: SQLite
-- Purpose: Store intelligence evolution, memory, and scoring
-- ==========================================================

PRAGMA foreign_keys = ON;

-- ==========================================================
-- TABLE 1: sessions
-- Each row = one intelligence lifecycle
-- ==========================================================
CREATE TABLE IF NOT EXISTS sessions (
    session_uuid TEXT PRIMARY KEY,
    mutation_level INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- TABLE 2: messages
-- Stores raw dialogue history
-- ==========================================================
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_uuid TEXT,
    role TEXT CHECK(role IN ('user','assistant','system')),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_uuid) REFERENCES sessions(session_uuid)
);

-- ==========================================================
-- TABLE 3: reasoning_snapshots
-- Stores internal cognition
-- ==========================================================
CREATE TABLE IF NOT EXISTS reasoning_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_uuid TEXT,
    
    raw_reasoning TEXT,           -- Full internal reasoning trace
    compressed_reasoning TEXT,    -- Output from CompressorAgent
    traits_json TEXT,             -- ObserverAgent output (tone, bias, depth)
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_uuid) REFERENCES sessions(session_uuid)
);

-- ==========================================================
-- TABLE 4: evaluations
-- Stores scoring and performance metrics
-- ==========================================================
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_uuid TEXT,

    accuracy REAL,
    clarity REAL,
    depth REAL,
    originality REAL,
    overall REAL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_uuid) REFERENCES sessions(session_uuid)
);

-- ==========================================================
-- TABLE 5 (OPTIONAL): session_traits
-- Tracks evolving personality profile
-- ==========================================================
CREATE TABLE IF NOT EXISTS session_traits (
    session_uuid TEXT PRIMARY KEY,

    creativity REAL,
    abstraction REAL,
    verbosity REAL,
    formality REAL,

    last_mutation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_uuid) REFERENCES sessions(session_uuid)
);

-- ==========================================================
-- INDEXES (Speed wins)
-- ==========================================================
CREATE INDEX IF NOT EXISTS idx_messages_session
ON messages (session_uuid);

CREATE INDEX IF NOT EXISTS idx_reasoning_session
ON reasoning_snapshots (session_uuid);

CREATE INDEX IF NOT EXISTS idx_evaluations_session
ON evaluations (session_uuid);
