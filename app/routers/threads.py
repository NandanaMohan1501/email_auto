from fastapi import APIRouter, HTTPException

from app import crud, schemas

router = APIRouter(
    prefix="/threads",
    tags=["Threads"]
)


@router.get("/", response_model=list[schemas.ThreadResponse])
def get_all_threads():

    return crud.get_threads()


@router.get("/{thread_id}", response_model=schemas.ThreadResponse)
def get_thread(thread_id: int):

    thread = crud.get_thread(thread_id)

    if thread is None:
        raise HTTPException(
            status_code=404,
            detail="Thread not found."
        )

    return thread


@router.get("/{thread_id}/emails",
            response_model=list[schemas.EmailResponse])
def get_thread_emails(thread_id: int):

    thread = crud.get_thread(thread_id)

    if thread is None:
        raise HTTPException(
            status_code=404,
            detail="Thread not found."
        )

    return crud.get_thread_emails(thread_id)