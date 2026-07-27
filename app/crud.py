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

#insert emails

def create_email(email):

    if get_email_by_message_id(email.message_id):
        return None

    result = classify_email(email.subject, email.body)

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

            OUTPUT INSERTED.id

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                email.mailbox,
                email.sender,
                email.subject,
                email.body,
                email.preview,
                email.received_on,
                email.conversation_id,
                email.message_id,
                email.status,
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