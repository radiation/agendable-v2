from typing import List

import crud
import db
from fastapi import APIRouter, Depends, Path
from schemas import meeting_attendee_schemas as meeting_attendee_schemas
from schemas import meeting_schemas as meeting_schemas
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# Create a new meeting attendee
@router.post("/", response_model=meeting_attendee_schemas.MeetingAttendee)
async def create_meeting_attendee(
    attendee: meeting_attendee_schemas.MeetingAttendeeBase,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_attendee_schemas.MeetingAttendee:
    return await crud.create_attendee(db, attendee=attendee)


# List all meeting attendees
@router.get("/", response_model=List[meeting_attendee_schemas.MeetingAttendee])
async def get_meeting_attendees(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(db.get_db),
) -> List[meeting_attendee_schemas.MeetingAttendee]:
    return await crud.get_attendees(db, skip=skip, limit=limit)


# Get a meeting attendee by ID
@router.get("/{attendee_id}", response_model=meeting_attendee_schemas.MeetingAttendee)
async def get_meeting_attendee(
    attendee_id: int = Path(..., description="The ID of the attendee to be retrieved"),
    db: AsyncSession = Depends(db.get_db),
) -> meeting_attendee_schemas.MeetingAttendee:
    return await crud.get_attendee(db, attendee_id=attendee_id)


# Update an existing meeting attendee
@router.put("/{attendee_id}", response_model=meeting_attendee_schemas.MeetingAttendee)
async def update_meeting_attendee(
    attendee_id: int,
    attendee: meeting_attendee_schemas.MeetingAttendeeUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_attendee_schemas.MeetingAttendee:
    return await crud.update_attendee(db, attendee_id=attendee_id, attendee=attendee)


# Delete a meeting attendee
@router.get(
    "/by_meeting/${meeting_id}",
    response_model=List[meeting_attendee_schemas.MeetingAttendee],
)
async def read_attendees_by_meeting(
    meeting_id: int = Path(
        ..., description="The ID of the meeting whose attendees are to be retrieved"
    ),
    db: AsyncSession = Depends(db.get_db),
) -> List[meeting_attendee_schemas.MeetingAttendee]:
    return await crud.get_attendees_by_meeting(db, meeting_id=meeting_id)


# Get all meetings for a specific user
@router.get("/user_meetings/{user_id}", response_model=List[meeting_schemas.Meeting])
async def read_meetings_by_user(
    user_id: int = Path(
        ..., description="The ID of the user whose meetings are to be retrieved"
    ),
    db: AsyncSession = Depends(db.get_db),
) -> List[meeting_schemas.Meeting]:
    return await crud.get_user_meetings(db, user_id=user_id)
