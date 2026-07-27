from app.db import get_cursor, SCHEMA

with get_cursor() as cur:

    cur.execute(
        f"""
        SELECT *
        FROM {SCHEMA}.Emails
        """
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)


        