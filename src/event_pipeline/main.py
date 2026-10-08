import sys
import time
from pathlib import Path

from event_pipeline.analytics import (
    get_events_by_source,
    get_events_by_type,
    get_hourly_activity,
    get_top_active_users,
    get_total_events,
    get_total_purchases,
    get_unique_users,
)
from event_pipeline.database import create_database, insert_events
from event_pipeline.deduplicator import remove_duplicates
from event_pipeline.logger import setup_logger
from event_pipeline.reader import read_events
from event_pipeline.reporter import save_csv_report, save_report
from event_pipeline.validator import validate_event


def main():
    logger = setup_logger()
    logger.info("Pipeline started")

    start_time = time.perf_counter()

    # input_path = Path("data/input/events.csv")
    if len(sys.argv) != 2:
        raise SystemExit(
           "Usage: uv run python src\\event_pipeline\\main.py <input_file>"
    )

    input_path = Path(sys.argv[1])
    database_path = Path("data/events.db")
    output_path = Path("data/output/report.json")
    csv_output_path = Path("data/output/report.csv")

    # 1. Read events
    data = read_events(input_path)
    records_received = len(data)

    logger.info("Records received: %s", records_received)

    # 2. Validate events
    valid_events = []
    invalid = 0

    for item in data:
        event, error = validate_event(item)

        if event:
            valid_events.append(event)
        else:
            invalid += 1
            logger.error(
                "Invalid event: %s | Error: %s",
                item,
                error,
            )

    logger.info("Valid records: %s", len(valid_events))
    logger.info("Invalid records: %s", invalid)

    # 3. Remove duplicates
    unique_events, duplicates = remove_duplicates(valid_events)

    logger.info("Duplicates: %s", duplicates)

    # 4. Store cleaned events in SQLite
    connection = create_database(database_path)
    insert_events(connection, unique_events)

    # 5. Calculate analytics
    report = {
        "records_received": records_received,
        "valid": len(valid_events),
        "invalid": invalid,
        "duplicates": duplicates,
        "total_events": get_total_events(connection),
        "unique_users": get_unique_users(connection),
        "total_purchases": get_total_purchases(connection),
        "events_by_type": get_events_by_type(connection),
        "events_by_source": get_events_by_source(connection),
        "top_active_users": get_top_active_users(connection),
        "hourly_activity": get_hourly_activity(connection),
    }

    # 6. Calculate processing time
    processing_time = time.perf_counter() - start_time

    report["processing_time_seconds"] = round(
        processing_time,
        4,
    )

    logger.info(
        "Processing time: %s seconds",
        report["processing_time_seconds"],
    )

    # 7. Save report
    save_report(report, output_path)
    save_csv_report(report, csv_output_path)

    logger.info(
       "JSON report generated: %s",
        output_path,
)

    logger.info(
    "CSV report generated: %s",
    csv_output_path,
)

    connection.close()

    # 8. Display summary
    print("\nProcessing completed!")
    print("--------------------------------")
    print(f"Records received : {records_received}")
    print(f"Valid records    : {len(valid_events)}")
    print(f"Invalid records  : {invalid}")
    print(f"Duplicates       : {duplicates}")
    print(f"Unique users     : {report['unique_users']}")
    print(f"Total purchases  : {report['total_purchases']}")
    print(f"Processing time  : {report['processing_time_seconds']} seconds")

if __name__ == "__main__":
    main()