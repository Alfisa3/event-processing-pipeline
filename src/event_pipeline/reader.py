import csv
import json
from pathlib import Path


def read_events(file_path: Path):
    if file_path.suffix.lower() == ".json":
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    if file_path.suffix.lower() == ".csv":
        with file_path.open("r", encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file))

    raise ValueError("Unsupported file format")


if __name__ == "__main__":
    file_path = Path("data/input/events.json")
    events = read_events(file_path)

    print(events)