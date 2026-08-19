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
    thread_id: int | None = None
    status: str
    category: str | None = None
    priority: str | None = None
    summary: str | None = None

    class Config:
        from_attributes = True

class ThreadResponse(BaseModel):
    thread_id: int
    conversation_id: str
    mailbox: str
    status: str
    summary: str | None = None

    class Config:
        from_attributes = True


class ConversationListItem(BaseModel):
    thread_id: int
    mailbox: str
    subject: str
    priority: str | None = None
    status: str | None = None
    category: str | None = None
    received_on: datetime

    class Config:
        from_attributes = True