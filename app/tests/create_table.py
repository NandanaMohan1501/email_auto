from app.db import get_cursor, SCHEMA

with get_cursor() as cur:

    # Threads table
    cur.execute(f"""

    CREATE TABLE {SCHEMA}.Threads(

        thread_id INT IDENTITY(1,1) PRIMARY KEY,

        conversation_id NVARCHAR(255) NOT NULL,

        mailbox NVARCHAR(100) NOT NULL,

        status NVARCHAR(100) DEFAULT 'Open',

        summary NVARCHAR(MAX),

        created_on DATETIME2 DEFAULT GETDATE(),

        updated_on DATETIME2 DEFAULT GETDATE(),

        CONSTRAINT UQ_Threads UNIQUE (conversation_id, mailbox)

    )

    """)

    # Emails table
    cur.execute(f"""

    CREATE TABLE {SCHEMA}.Emails(

        id INT IDENTITY(1,1) PRIMARY KEY,

        thread_id INT NULL,

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

        summary NVARCHAR(MAX),

        CONSTRAINT FK_Emails_Threads
        FOREIGN KEY(thread_id)
        REFERENCES {SCHEMA}.Threads(thread_id)

    )

    """)

print("Tables created.")