import sqlite3
from pathlib import Path


def create_database(db_path: Path):
    connection = sqlite3.connect(db_path)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL
        )
        """
    )

    connection.execute("DELETE FROM events")

    connection.commit()

    return connection


def insert_events(connection, events):
    for event in events:
        connection.execute(
            """
            INSERT OR IGNORE INTO events (
                event_id,
                user_id,
                event_type,
                timestamp,
                source
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.user_id,
                event.event_type,
                event.timestamp.isoformat(),
                event.source,
            ),
        )

    connection.commit()


if __name__ == "__main__":
    db_path = Path("data/events.db")

    connection = create_database(db_path)

    print("Database created successfully!")

    connection.close()