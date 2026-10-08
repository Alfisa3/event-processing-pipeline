import csv
import json
from pathlib import Path


def save_report(report, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

def save_csv_report(report, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Metric", "Value"])

        writer.writerow(["Records Received", report["records_received"]])
        writer.writerow(["Valid", report["valid"]])
        writer.writerow(["Invalid", report["invalid"]])
        writer.writerow(["Duplicates", report["duplicates"]])
        writer.writerow(["Total Events", report["total_events"]])
        writer.writerow(["Unique Users", report["unique_users"]])
        writer.writerow(["Total Purchases", report["total_purchases"]])
        writer.writerow([
            "Processing Time (seconds)",
            report["processing_time_seconds"]
        ])        


if __name__ == "__main__":
    report = {
        "total_events": 3,
        "unique_users": 2,
        "events_by_type": {
            "login": 1,
            "logout": 1,
            "purchase": 1
        },
        "events_by_source": {
            "mobile": 2,
            "web": 1
        }
    }

    output_path = Path("data/output/report.json")

    save_report(report, output_path)

    print("Report saved successfully!")        