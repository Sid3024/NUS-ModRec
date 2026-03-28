from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any


DB_PATH = Path("data") / "app.db"


def init_audit_db() -> None:
    """
    Creates the SQLite database and recommendation_events table if needed.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS recommendation_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                request_id TEXT NOT NULL,
                session_id TEXT,
                major TEXT,
                success INTEGER NOT NULL,
                num_jobs INTEGER NOT NULL,
                num_mods_returned INTEGER NOT NULL,
                ambiguity_agent_used INTEGER NOT NULL,
                fallback_used INTEGER NOT NULL,
                latency_ms INTEGER NOT NULL,
                error_message TEXT,
                event_json TEXT NOT NULL
            )
        """)
        conn.commit()


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def log_recommendation_event(event: dict[str, Any]) -> None:
    """
    Stores one full recommendation event in SQLite.
    Also stores key summary fields in dedicated columns for easy querying.
    """

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO recommendation_events (
                timestamp,
                request_id,
                session_id,
                major,
                success,
                num_jobs,
                num_mods_returned,
                ambiguity_agent_used,
                fallback_used,
                latency_ms,
                error_message,
                event_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.get("timestamp"),
                event.get("request_id"),
                event.get("session_id"),
                event.get("major"),
                1 if event.get("success", False) else 0,
                len(event.get("jobs", [])),
                len(event.get("recommended_mods", [])),
                1 if event.get("ambiguity_agent_used", False) else 0,
                1 if event.get("fallback_used", False) else 0,
                int(event.get("latency_ms", 0)),
                event.get("error_message"),
                json.dumps(event, ensure_ascii=False),
            ),
        )
        conn.commit()