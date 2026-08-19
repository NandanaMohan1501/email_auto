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


def get_dashboard_threads(
    mailbox=None,
    priority=None,
    status=None,
    category=None,
    sender=None,
    from_date=None,
    to_date=None,
):
    query = f"""
    WITH LatestEmails AS
    (
        SELECT
            e.*,
            ROW_NUMBER() OVER (
                PARTITION BY e.thread_id
                ORDER BY e.received_on DESC, e.id DESC
            ) AS row_number
        FROM {SCHEMA}.Emails e
        WHERE e.thread_id IS NOT NULL
    )
    SELECT
        thread_id,
        mailbox,
        subject,
        priority,
        status,
        category,
        received_on
    FROM LatestEmails
    WHERE row_number = 1
    """
    params = []

    if mailbox and mailbox.lower() != "all":
        query += " AND mailbox = ?"
        params.append(mailbox)

    if priority:
        query += " AND priority = ?"
        params.append(priority)

    if status:
        query += " AND status = ?"
        params.append(status)

    if category:
        query += " AND category = ?"
        params.append(category)

    if sender:
        query += " AND sender = ?"
        params.append(sender)

    if from_date:
        query += " AND received_on >= ?"
        params.append(from_date)

    if to_date:
        query += " AND received_on < DATEADD(day, 1, ?)"
        params.append(to_date)

    query += " ORDER BY received_on DESC, thread_id DESC"

    with get_cursor() as cur:
        cur.execute(query, tuple(params))
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

def get_emails(mailbox=None,
            priority=None,
            status=None,
            category=None,
            sender=None,
            from_date=None,
            to_date=None,):

    query = f"""
    SELECT *
    FROM {SCHEMA}.Emails
    WHERE 1=1
    """
    params = []

    if mailbox and mailbox.lower() != "all":
        query += " AND mailbox=?"
        params.append(mailbox)

    if priority:
        query += " AND priority=?"
        params.append(priority)

    if status:
        query += " AND status=?"
        params.append(status)
    if category:
        query += " AND category=?"
        params.append(category)
    if sender:
        query += " AND sender=?"
        params.append(sender)

    if from_date:
        query += " AND received_on >= ?"
        params.append(from_date)
        
    if to_date:
        query += " AND received_on < DATEADD(day, 1, ?)"
        params.append(to_date)


    query += " ORDER BY received_on DESC"

    with get_cursor() as cur:
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        return [row_to_dict(cur, row) for row in rows]


def get_mailboxes():
    return [
        "careers",
        "operations",
        "info",
        "hr",
        "support",
        "sales",
        # add the remaining names to make 9
    ]

def get_priorities():
    return ["High", "Medium", "Low"]


def get_statuses():
    with get_cursor() as cur:
        cur.execute(
            f"""
            SELECT DISTINCT status
            FROM {SCHEMA}.Emails
            WHERE status IS NOT NULL AND status <> ''
            ORDER BY status
            """
        )
        return [row[0] for row in cur.fetchall()]


def get_categories():
    with get_cursor() as cur:
        cur.execute(
            f"""
            SELECT DISTINCT category
            FROM {SCHEMA}.Emails
            WHERE category IS NOT NULL AND category <> ''
            ORDER BY category
            """
        )
        return [row[0] for row in cur.fetchall()]

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