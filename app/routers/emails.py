from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud

router = APIRouter(
    prefix="/emails",
    tags=["Emails"]
)


@router.post("/", response_model=schemas.EmailResponse)
def create_email(email: schemas.EmailCreate, db: Session = Depends(get_db)):
    created_email = crud.create_email(db, email)

    if created_email is None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists."
        )

    return created_email

@router.get("/", response_model=list[schemas.EmailResponse])
def get_all_emails(db: Session = Depends(get_db)):
    return crud.get_emails(db)


@router.get("/{email_id}", response_model=schemas.EmailResponse)
def get_email(email_id: int, db: Session = Depends(get_db)):
    return crud.get_email(db, email_id)






