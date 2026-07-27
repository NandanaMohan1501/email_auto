from app.db import get_cursor, SCHEMA

with get_cursor() as cur:

    cur.execute(
        f"""
        INSERT INTO {SCHEMA}.Emails
        (
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
        (?, ?, ?, ?, ?, GETDATE(), ?, ?, ?, ?, ?, ?)

        """,

        (
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