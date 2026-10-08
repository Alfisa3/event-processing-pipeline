def get_total_events(connection):
    result = connection.execute(
        "SELECT COUNT(*) FROM events"
    ).fetchone()

    return result[0]


def get_unique_users(connection):
    result = connection.execute(
        "SELECT COUNT(DISTINCT user_id) FROM events"
    ).fetchone()

    return result[0]


def get_total_purchases(connection):
    result = connection.execute(
        """
        SELECT COUNT(*)
        FROM events
        WHERE event_type = 'purchase'
        """
    ).fetchone()

    return result[0]


def get_events_by_type(connection):
    rows = connection.execute(
        """
        SELECT event_type, COUNT(*)
        FROM events
        GROUP BY event_type
        """
    ).fetchall()

    return dict(rows)


def get_events_by_source(connection):
    rows = connection.execute(
        """
        SELECT source, COUNT(*)
        FROM events
        GROUP BY source
        """
    ).fetchall()

    return dict(rows)


def get_top_active_users(connection, limit=10):
    rows = connection.execute(
        """
        SELECT user_id, COUNT(*) AS event_count
        FROM events
        GROUP BY user_id
        ORDER BY event_count DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    return [
        {"user_id": user_id, "event_count": event_count}
        for user_id, event_count in rows
    ]


def get_hourly_activity(connection):
    rows = connection.execute(
        """
        SELECT
            substr(timestamp, 12, 2) AS hour,
            COUNT(*) AS event_count
        FROM events
        GROUP BY hour
        ORDER BY hour
        """
    ).fetchall()

    return [
        {"hour": hour, "event_count": event_count}
        for hour, event_count in rows
    ]


if __name__ == "__main__":
    import sqlite3

    connection = sqlite3.connect("data/events.db")

    print("Total events:", get_total_events(connection))
    print("Unique users:", get_unique_users(connection))
    print("Total purchases:", get_total_purchases(connection))
    print("Events by type:", get_events_by_type(connection))
    print("Events by source:", get_events_by_source(connection))
    print("Top active users:", get_top_active_users(connection))
    print("Hourly activity:", get_hourly_activity(connection))

    connection.close()