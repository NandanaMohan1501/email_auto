from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routers import emails,threads



app = FastAPI(        #Creates the root app = FastAPI(...) instance.
    title="Email Management API"
)

app.include_router(emails.router)
app.include_router(threads.router)


@app.get("/demo", include_in_schema=False)
def demo():
    return FileResponse(Path(__file__).parent / "app" / "frontend.html")


@app.get("/")
def home():
    return {
        "message": "Email Management API"
    }