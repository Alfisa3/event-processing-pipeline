from event_pipeline.validator import validate_event


def test_valid_event():
    data = {
        "event_id": "e5001",
        "user_id": "u501",
        "event_type": "login",
        "timestamp": "2026-10-07T10:00:00Z",
        "source": "web",
    }

    event, error = validate_event(data)

    assert event is not None
    assert error is None


def test_invalid_event():
    data = {
        "event_id": "e5002",
        "user_id": "",
        "event_type": "login",
        "timestamp": "2026-10-07T10:00:00Z",
        "source": "web",
    }

    event, error = validate_event(data)

    assert event is None
    assert error is not None    