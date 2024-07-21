from app.routers import (
    meeting_attendee_router,
    meeting_recurrence_router,
    meeting_router,
    meeting_task_router,
    task_router,
)
from fastapi import FastAPI

app = FastAPI()

# Include routers that might use the database internally
app.include_router(meeting_router.router, prefix="/meetings", tags=["meetings"])
app.include_router(task_router.router, prefix="/tasks", tags=["tasks"])
app.include_router(
    meeting_task_router.router, prefix="/meeting_tasks", tags=["meeting_tasks"]
)
app.include_router(
    meeting_attendee_router.router,
    prefix="/meeting_attendees",
    tags=["meeting_attendees"],
)
app.include_router(
    meeting_recurrence_router.router,
    prefix="/meeting_recurrences",
    tags=["meeting_recurrences"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Meeting Service API"}
