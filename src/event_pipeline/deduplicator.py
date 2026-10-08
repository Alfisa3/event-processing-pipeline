def remove_duplicates(events):
    seen = set()
    unique_events = []
    duplicates = 0

    for event in events:
        if event.event_id in seen:
            duplicates += 1
        else:
            seen.add(event.event_id)
            unique_events.append(event)

    return unique_events, duplicates


if __name__ == "__main__":
    from pathlib import Path

    from event_pipeline.reader import read_events
    from event_pipeline.validator import validate_event

    file_path = Path("data/input/events.json")
    data = read_events(file_path)

    events = []

    for item in data:
        event = validate_event(item)

        if event:
            events.append(event)

    unique_events, duplicates = remove_duplicates(events)

    print("Unique events:", len(unique_events))
    print("Duplicates:", duplicates)