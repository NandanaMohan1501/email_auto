from app.db import get_cursor, SCHEMA

with get_cursor() as cur:

    # Insert thread
    cur.execute(
        f"""
        INSERT INTO {SCHEMA}.Threads
        (
            conversation_id,
            mailbox,
            status,
            summary
        )

        VALUES (?, ?, ?, ?)
        """,
        (
            "conv001",
            "careers",
            "Open",
            "Test Thread"
        )
    )

    # Get generated thread_id
    cur.execute(
        f"""
        SELECT thread_id
        FROM {SCHEMA}.Threads
        WHERE conversation_id=?
        AND mailbox=?
        """,
        (
            "conv001",
            "careers"
        )
    )

    thread_id = cur.fetchone()[0]

    # Insert email
    cur.execute(
        f"""
        INSERT INTO {SCHEMA}.Emails
        (
            thread_id,
            mailbox,
            sender,
            subject,
            body,
            preview,
            received_on,
            conversation_id,
            message_id,
            status,
            category,
            priority,
            summary
        )

        VALUES
        (?, ?, ?, ?, ?, ?, GETDATE(), ?, ?, ?, ?, ?, ?)
        """,
        (
            thread_id,
            "careers",
            "test@test.com",
            "Testing",
            "Testing Azure SQL",
            "Preview",
            "conv001",
            "msg001",
            "New",
            "TEST_CATEGORY",
            "TEST_PRIORITY",
            "TEST_SUMMARY"
        )
    )

print("Insert successful.")