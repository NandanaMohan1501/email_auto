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
def get_all_emails():

    return crud.get_emails()


@router.get("/{email_id}", response_model=schemas.EmailResponse)
def get_email(email_id: int):

    email = crud.get_email(email_id)

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found."
        )

    return email