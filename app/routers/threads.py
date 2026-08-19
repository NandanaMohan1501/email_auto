from datetime import date

from fastapi import APIRouter, HTTPException

from app import crud, schemas

router = APIRouter(
    prefix="/threads",
    tags=["Threads"]
)


@router.get("/", response_model=list[schemas.ThreadResponse])
def get_all_threads():

    return crud.get_threads()


@router.get("/dashboard", response_model=list[schemas.ConversationListItem])
def get_dashboard_threads(
    mailbox: str | None = None,
    priority: str | None = None,
    status: str | None = None,
    category: str | None = None,
    sender: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
):
    if from_date and to_date and from_date > to_date:
        raise HTTPException(
            status_code=400,
            detail="from_date cannot be later than to_date.",
        )

    return crud.get_dashboard_threads(
        mailbox=mailbox,
        priority=priority,
        status=status,
        category=category,
        sender=sender,
        from_date=from_date,
        to_date=to_date,
    )


@router.get("/{thread_id}", response_model=schemas.ThreadResponse)
def get_thread(thread_id: int):

    thread = crud.get_thread(thread_id)

    if thread is None:
        raise HTTPException(
            status_code=404,
            detail="Thread not found."
        )

    return thread


@router.get("/{thread_id}/emails",
            response_model=list[schemas.EmailResponse])
def get_thread_emails(thread_id: int):

    thread = crud.get_thread(thread_id)

    if thread is None:
        raise HTTPException(
            status_code=404,
            detail="Thread not found."
        )

    return crud.get_thread_emails(thread_id)