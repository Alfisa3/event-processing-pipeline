from pydantic import ValidationError

from event_pipeline.models import Event


def validate_event(data):
    try:
        event = Event(**data)
        return event, None

    except ValidationError as error:
        return None, str(error)


if __name__ == "__main__":
    from pathlib import Path

    from event_pipeline.reader import read_events

    file_path = Path("data/input/events.json")
    events = read_events(file_path)

    valid = 0
    invalid = 0

    for data in events:
        event, error = validate_event(data)

        if event:
            valid += 1
        else:
            invalid += 1
            print("Invalid event:", error)

    print("Valid:", valid)
    print("Invalid:", invalid)