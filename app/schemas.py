#validates incoming data

from pydantic import BaseModel
from datetime import datetime


class EmailCreate(BaseModel):
    mailbox: str
    sender: str
    subject: str
    body: str
    preview: str
    received_on: datetime
    conversation_id: str
    message_id: str


class EmailResponse(EmailCreate):
    id: int
    status: str
    category: str | None = None
    priority: str | None = None
    summary: str | None = None

    class Config:
        from_attributes = True