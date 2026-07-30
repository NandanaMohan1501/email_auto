from app.db import get_cursor, SCHEMA
from app.services.classifier import classify_email



def row_to_dict(cursor, row):
    if row is None:
        return None

    columns = [column[0] for column in cursor.description]

    return dict(zip(columns, row))

#duplicate check 

def get_email_by_message_id(message_id: str):

    with get_cursor() as cur:

        cur.execute(
            f"""
            SELECT *
            FROM {SCHEMA}.Emails
            WHERE message_id=?
            """,
            (message_id,),
        )

        row = cur.fetchone()

        return row_to_dict(cur, row)

# ---------- THREADS ----------

def get_thread_by_conversation_id(conversation_id: str, mailbox: str):

    with get_cursor() as cur:

        cur.execute(
            f"""
            SELECT *
            FROM {SCHEMA}.Threads
            WHERE conversation_id = ?
            AND mailbox = ?
            """,
            (conversation_id, mailbox),
        )

        row = cur.fetchone()

        return row_to_dict(cur, row)


def create_thread(conversation_id: str, mailbox: str):

    with get_cursor() as cur:

        cur.execute(
            f"""
            INSERT INTO {SCHEMA}.Threads
            (
                conversation_id,
                mailbox,
                status
            )

            OUTPUT INSERTED.thread_id

            VALUES (?, ?, ?)
            """,
            (
                conversation_id,
                mailbox,
                "Open",
            ),
        )

        return cur.fetchone()[0]


def get_threads():

    with get_cursor() as cur:

        cur.execute(
            f"""
            SELECT *
            FROM {SCHEMA}.Threads
            ORDER BY updated_on DESC
            """
        )

        rows = cur.fetchall()

        return [row_to_dict(cur, row) for row in rows]


def get_thread(thread_id: int):

    with get_cursor() as cur:

        cur.execute(
            f"""
            SELECT *
            FROM {SCHEMA}.Threads
            WHERE thread_id = ?
            """,
            (thread_id,),
        )

        row = cur.fetchone()

        return row_to_dict(cur, row)


def get_thread_emails(thread_id: int):

    with get_cursor() as cur:

        cur.execute(
            f"""
            SELECT *
            FROM {SCHEMA}.Emails
            WHERE thread_id = ?
            ORDER BY received_on ASC
            """,
            (thread_id,),
        )

        rows = cur.fetchall()

        return [row_to_dict(cur, row) for row in rows]


















#insert emails

def create_email(email):

    if get_email_by_message_id(email.message_id):
        return None

    thread = get_thread_by_conversation_id(
        email.conversation_id,
        email.mailbox,
    )

    if thread:
        thread_id = thread["thread_id"]
    else:
        thread_id = create_thread(
            email.conversation_id,
            email.mailbox,
        )

    result = classify_email(email.subject, email.body)

    with get_cursor() as cur:

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

            OUTPUT INSERTED.id

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
            thread_id,
            email.mailbox,
            email.sender,
            email.subject,
            email.body,
            email.preview,
            email.received_on,
            email.conversation_id,
            email.message_id,
            "New",         
            result["category"],
            result["priority"],
            result["summary"],
),
        )

        new_id = cur.fetchone()[0]

    return get_email(new_id)

#get all emails

def get_emails():

    with get_cursor() as cur:

        cur.execute(
            f"""
            SELECT *
            FROM {SCHEMA}.Emails
            ORDER BY received_on DESC
            """
        )

        rows = cur.fetchall()

        return [row_to_dict(cur, row) for row in rows]
#get one email

def get_email(email_id: int):

    with get_cursor() as cur:

        cur.execute(
            f"""
            SELECT *
            FROM {SCHEMA}.Emails
            WHERE id=?
            """,
            (email_id,),
        )

        row = cur.fetchone()

        return row_to_dict(cur, row)