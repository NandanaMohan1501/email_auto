from fastapi import APIRouter, HTTPException

from app import schemas, crud

router = APIRouter(
    prefix="/emails",
    tags=["Emails"]
)


@router.post("/", response_model=schemas.EmailResponse)
def create_email(email: schemas.EmailCreate):

    created_email = crud.create_email(email)

    if created_email is None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists."
        )

    return created_email


@router.get("/", response_model=list[schemas.EmailResponse])
def get_all_emails(
    mailbox: str | None = None,
    priority: str | None = None,
    status: str | None = None,
    category: str | None = None,
    sender: str | None = None):

    return crud.get_emails(
        mailbox=mailbox,
        priority=priority,
        status=status,
        category=category,
        sender=sender)

@router.get("/mailboxes", response_model=list[str])
def get_mailboxes():
    return crud.get_mailboxes()


@router.get("/priorities", response_model=list[str])
def get_priorities():
    return crud.get_priorities()


@router.get("/statuses", response_model=list[str])
def get_statuses():
    return crud.get_statuses()


@router.get("/categories", response_model=list[str])
def get_categories():
    return crud.get_categories()

@router.get("/{email_id}", response_model=schemas.EmailResponse)
def get_email(email_id: int):

    email = crud.get_email(email_id)

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found."
        )

    return email