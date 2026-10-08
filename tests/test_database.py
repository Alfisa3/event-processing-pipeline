from event_pipeline.database import create_database, insert_events
from event_pipeline.models import Event


def test_insert_events(tmp_path):
    db_path = tmp_path / "test.db"

    connection = create_database(db_path)

    events = [
        Event(
            event_id="e6001",
            user_id="u601",
            event_type="login",
            timestamp="2026-10-07T10:00:00Z",
            source="web",
        )
    ]

    insert_events(connection, events)

    result = connection.execute(
        "SELECT COUNT(*) FROM events"
    ).fetchone()

    assert result[0] == 1

    connection.close()