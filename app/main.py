from fastapi import FastAPI

from app.db import engine
from app.models import Base
from app.routers import emails

Base.metadata.create_all(bind=engine)  # automatically creates the SQLite database

app = FastAPI(        #Creates the root app = FastAPI(...) instance.
    title="Email Management API"
)

app.include_router(emails.router)


@app.get("/")
def home():
    return {
        "message": "Email Management API"
    }