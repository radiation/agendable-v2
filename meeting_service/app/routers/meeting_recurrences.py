import crud
import db
from fastapi import APIRouter, Depends
from schemas import meeting_task_schemas as schemas
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# Create a new meeting recurrence
@router.post("/", response_model=schemas.MeetingTask)
async def create_meeting_recurrence(
    meeting_recurrence: schemas.MeetingTaskCreate,
    db: AsyncSession = Depends(db.get_db),
) -> schemas.MeetingTask:
    return await crud.create_meeting_recurrence(
        db=db, meeting_recurrence=meeting_recurrence
    )


# List all meeting recurrences
@router.get("/", response_model=list[schemas.MeetingTask])
async def get_meeting_recurrences(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> list[schemas.MeetingTask]:
    return await crud.get_meeting_recurrences(db=db, skip=skip, limit=limit)


# Get a meeting recurrence by ID
@router.get("/${meeting_id}", response_model=schemas.MeetingTask)
async def get_meeting_recurrence(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
) -> schemas.MeetingTask:
    return await crud.get_meeting_recurrence(db=db, meeting_id=meeting_id)


# Update an existing meeting recurrence
@router.put("/{meeting_id}", response_model=schemas.MeetingTask)
async def update_meeting_recurrence(
    meeting_id: int,
    meeting_recurrence: schemas.MeetingTaskUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> schemas.MeetingTask:
    return await crud.update_meeting_recurrence(
        db=db, meeting_id=meeting_id, meeting_recurrence=meeting_recurrence
    )


# Delete a meeting recurrence
@router.delete("/{meeting_id}")
async def delete_meeting_recurrence(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
):
    return await crud.delete_meeting_recurrence(db=db, meeting_id=meeting_id)


# Get the meeting recurrence Attached to a meeting
@router.get(
    "/by_meeting/${meeting_id}",
    response_model=list[schemas.MeetingTask],
)
async def get_meeting_recurrences_by_meeting(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
) -> list[schemas.MeetingTask]:
    return await crud.get_meeting_recurrences_by_meeting(db=db, meeting_id=meeting_id)
