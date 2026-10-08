from event_pipeline.deduplicator import remove_duplicates
from event_pipeline.models import Event


def test_remove_duplicates():
    events = [
        Event(
            event_id="e5001",
            user_id="u501",
            event_type="login",
            timestamp="2026-10-07T10:00:00Z",
            source="web",
        ),
        Event(
            event_id="e5001",
            user_id="u501",
            event_type="login",
            timestamp="2026-10-07T10:00:00Z",
            source="web",
        ),
    ]

    unique_events, duplicates = remove_duplicates(events)

    assert len(unique_events) == 1
    assert duplicates == 1