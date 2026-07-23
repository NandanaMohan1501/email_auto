#talks to sqlite

from sqlalchemy.orm import Session
from app import models, schemas
from app.services.classifier import classify_email

def create_email(db: Session, email: schemas.EmailCreate):



    #Checks for duplication using the unique message_id.
    #Inserts the new email into the SQLite database  
    #classify_email:asynchronously to obtain AI-generated classification tags.
    #Updates and saves the category, priority, and summary directly back to the database row.

    existing_email = get_email_by_message_id(db, email.message_id)

    if existing_email:
        return None

    db_email = models.Email(**email.model_dump())

    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    classification = classify_email(
    db_email.subject,
    db_email.body
    )

    db_email.category = classification["category"]

    db_email.priority = classification["priority"]

    db_email.summary = classification["summary"]

    db.commit()

    db.refresh(db_email)


    return db_email

def get_emails(db: Session):
    return db.query(models.Email).all()

def get_email(db: Session, email_id: int):
    return db.query(models.Email).filter(models.Email.id == email_id).first()

def get_email_by_message_id(db: Session, message_id: str):
    return (
        db.query(models.Email)
        .filter(models.Email.message_id == message_id)
        .first()
    )