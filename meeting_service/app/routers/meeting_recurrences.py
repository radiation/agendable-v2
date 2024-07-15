import crud
import db
from fastapi import APIRouter, Depends, HTTPException
from schemas import meeting_recurrence_schemas
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Create a new meeting recurrence
@router.post("/", response_model=meeting_recurrence_schemas.MeetingRecurrence)
async def create_meeting_recurrence(
    meeting_recurrence: meeting_recurrence_schemas.MeetingRecurrenceCreate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_recurrence_schemas.MeetingRecurrence:
    return await crud.create_meeting_recurrence(
        db=db, meeting_recurrence=meeting_recurrence
    )


# List all meeting recurrences
@router.get("/", response_model=list[meeting_recurrence_schemas.MeetingRecurrence])
async def get_meeting_recurrences(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> list[meeting_recurrence_schemas.MeetingRecurrence]:
    return await crud.get_meeting_recurrences(db=db, skip=skip, limit=limit)


# Get a meeting recurrence by ID
@router.get(
    "/{meeting_id}", response_model=meeting_recurrence_schemas.MeetingRecurrence
)
async def get_meeting_recurrence(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
) -> meeting_recurrence_schemas.MeetingRecurrence:
    recurrence = await crud.get_meeting_recurrence(db=db, meeting_id=meeting_id)
    if recurrence is None:
        raise HTTPException(status_code=404, detail="Meeting recurrence not found")
    return recurrence


# Update an existing meeting recurrence
@router.put(
    "/{meeting_id}", response_model=meeting_recurrence_schemas.MeetingRecurrence
)
async def update_meeting_recurrence(
    meeting_id: int,
    meeting_recurrence: meeting_recurrence_schemas.MeetingRecurrenceUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_recurrence_schemas.MeetingRecurrence:
    return await crud.update_meeting_recurrence(
        db=db, meeting_id=meeting_id, meeting_recurrence=meeting_recurrence
    )


# Delete a meeting recurrence
@router.delete("/{meeting_id}", status_code=204)
async def delete_meeting_recurrence(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
):
    await crud.delete_meeting_recurrence(db=db, meeting_id=meeting_id)
    return {"detail": "Meeting recurrence deleted successfully"}


# Get the meeting recurrence attached to a meeting
@router.get(
    "/by_meeting/{meeting_id}",
    response_model=list[meeting_recurrence_schemas.MeetingRecurrence],
)
async def get_meeting_recurrences_by_meeting(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
) -> list[meeting_recurrence_schemas.MeetingRecurrence]:
    return await crud.get_meeting_recurrences_by_meeting(db=db, meeting_id=meeting_id)
