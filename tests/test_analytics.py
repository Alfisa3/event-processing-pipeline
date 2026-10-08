import sqlite3

from event_pipeline.analytics import (
    get_total_events,
    get_total_purchases,
    get_unique_users,
)


def test_analytics():
    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE events (
            event_id TEXT PRIMARY KEY,
            user_id TEXT,
            event_type TEXT,
            timestamp TEXT,
            source TEXT
        )
        """
    )

    connection.executemany(
        """
        INSERT INTO events (
            event_id,
            user_id,
            event_type,
            timestamp,
            source
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                "e7001",
                "u701",
                "login",
                "2026-10-07T10:00:00Z",
                "web",
            ),
            (
                "e7002",
                "u701",
                "purchase",
                "2026-10-07T10:10:00Z",
                "web",
            ),
            (
                "e7003",
                "u702",
                "purchase",
                "2026-10-07T10:20:00Z",
                "mobile",
            ),
        ],
    )

    assert get_total_events(connection) == 3
    assert get_unique_users(connection) == 2
    assert get_total_purchases(connection) == 2

    connection.close()