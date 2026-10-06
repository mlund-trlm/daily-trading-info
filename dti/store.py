"""SQLite store for drafts and their review/send lifecycle."""

import json
import os
import sqlite3
from contextlib import closing
from dataclasses import asdict

from dti.reports.base import Draft

DEFAULT_DB = os.environ.get("DTI_DB", "dti.sqlite3")

SCHEMA = """
CREATE TABLE IF NOT EXISTS drafts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    report      TEXT NOT NULL,
    run_date    TEXT NOT NULL,
    subject     TEXT NOT NULL,
    html        TEXT NOT NULL,
    sources     TEXT NOT NULL,           -- JSON list of URLs
    flags       TEXT NOT NULL,           -- JSON list of {message, item}
    empty       INTEGER NOT NULL,
    status      TEXT NOT NULL DEFAULT 'needs_review',  -- needs_review | approved | sent | skipped
    created_at  TEXT NOT NULL,
    reviewed_by TEXT,
    sent_at     TEXT
);
CREATE INDEX IF NOT EXISTS drafts_by_day ON drafts (run_date, report);
"""


def connect(path: str = DEFAULT_DB) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def save_draft(conn: sqlite3.Connection, draft: Draft) -> int:
    with conn:
        cur = conn.execute(
            "INSERT INTO drafts (report, run_date, subject, html, sources, flags, empty, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                draft.report,
                draft.run_date.isoformat(),
                draft.subject,
                draft.html,
                json.dumps(draft.sources),
                json.dumps([asdict(f) for f in draft.flags]),
                int(draft.empty),
                draft.created_at.isoformat(),
            ),
        )
    return cur.lastrowid


def drafts_for_day(conn: sqlite3.Connection, run_date: str) -> list[sqlite3.Row]:
    with closing(conn.execute(
        "SELECT * FROM drafts WHERE run_date = ? ORDER BY report, created_at DESC", (run_date,)
    )) as cur:
        return cur.fetchall()
