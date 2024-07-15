from fastapi import FastAPI
from routers import (
    meeting_attendees,
    meeting_recurrences,
    meeting_tasks,
    meetings,
    tasks,
)

app = FastAPI()

# Include routers that might use the database internally
app.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(
    meeting_tasks.router, prefix="/meeting_tasks", tags=["meeting_tasks"]
)
app.include_router(
    meeting_attendees.router, prefix="/meeting_attendees", tags=["meeting_attendees"]
)
app.include_router(
    meeting_recurrences.router,
    prefix="/meeting_recurrences",
    tags=["meeting_recurrences"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Meeting Service API"}
