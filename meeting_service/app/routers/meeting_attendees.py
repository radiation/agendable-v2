from typing import List

import crud
import db
from fastapi import APIRouter, Depends
from schemas import meeting_attendee_schemas as meeting_attendee_schemas
from schemas import meeting_schemas as meeting_schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/meeting_attendees/", response_model=List[meeting_attendee_schemas.MeetingAttendee]
)
def read_attendees_by_meeting(
    meeting_id: int, db: Session = Depends(db.get_db)
) -> List[meeting_attendee_schemas.MeetingAttendee]:
    return crud.get_attendees_by_meeting(db, meeting_id=meeting_id)


@router.get("/user_meetings/", response_model=List[meeting_schemas.Meeting])
def read_meetings_by_user(
    user_id: int, db: Session = Depends(db.get_db)
) -> List[meeting_schemas.Meeting]:
    return crud.get_user_meetings(db, user_id=user_id)
