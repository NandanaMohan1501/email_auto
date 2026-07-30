from fastapi import FastAPI
from app.routers import emails,threads



app = FastAPI(        #Creates the root app = FastAPI(...) instance.
    title="Email Management API"
)

app.include_router(emails.router)
app.include_router(threads.router)


@app.get("/")
def home():
    return {
        "message": "Email Management API"
    }