from app.db import get_cursor, SCHEMA

with get_cursor() as cur:

    print("\nTHREADS\n")

    cur.execute(
        f"""
        SELECT *
        FROM {SCHEMA}.Threads
        """
    )

    for row in cur.fetchall():
        print(row)

    print("\nEMAILS\n")

    cur.execute(
        f"""
        SELECT *
        FROM {SCHEMA}.Emails
        """
    )

    for row in cur.fetchall():
        print(row)