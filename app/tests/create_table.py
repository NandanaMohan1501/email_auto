from app.db import get_cursor, SCHEMA

with get_cursor() as cur:

    cur.execute(f"""

    CREATE TABLE {SCHEMA}.Emails(

        id INT IDENTITY(1,1) PRIMARY KEY,

        mailbox NVARCHAR(100),

        sender NVARCHAR(255),

        subject NVARCHAR(MAX),

        body NVARCHAR(MAX),

        preview NVARCHAR(MAX),

        received_on DATETIME2,

        conversation_id NVARCHAR(255),

        message_id NVARCHAR(255) UNIQUE,

        status NVARCHAR(100),

        category NVARCHAR(100),

        priority NVARCHAR(100),

        summary NVARCHAR(MAX)

    )

    """)

print("Table created.")