# defines schema of db table 

from sqlalchemy import Column, Integer, String, DateTime, Text
from app.db import Base

class Email(Base):

    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)

    mailbox = Column(String, nullable=False)

    sender = Column(String, nullable=False)

    subject = Column(String, nullable=False)

    body = Column(Text)

    preview = Column(Text)

    received_on = Column(DateTime)

    conversation_id = Column(String)

    message_id = Column(String, unique=True)

    status = Column(String, default="New", nullable=False)
    category = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    summary = Column(Text, nullable=True)