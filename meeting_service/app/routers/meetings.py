import crud.meeting_crud as crud
import db
from fastapi import APIRouter, Depends, HTTPException
from schemas import meeting_recurrence_schemas, meeting_schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=meeting_schemas.Meeting)
def create_meeting(
    meeting: meeting_schemas.MeetingCreate, db: Session = Depends(db.get_db)
) -> meeting_schemas.Meeting:
    return crud.create_meeting(db=db, meeting=meeting)


@router.get("/", response_model=list[meeting_schemas.Meeting])
def read_meetings(
    skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)
) -> list[meeting_schemas.Meeting]:
    return crud.get_meetings(db=db, skip=skip, limit=limit)


@router.get("/{meeting_id}", response_model=meeting_schemas.Meeting)
def read_meeting(
    meeting_id: int, db: Session = Depends(db.get_db)
) -> meeting_schemas.Meeting:
    db_meeting = crud.get_meeting(db=db, meeting_id=meeting_id)
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return db_meeting


@router.put("/{meeting_id}", response_model=meeting_schemas.Meeting)
def update_meeting(
    meeting_id: int,
    meeting: meeting_schemas.MeetingUpdate,
    db: Session = Depends(db.get_db),
) -> meeting_schemas.Meeting:
    return crud.update_meeting(db=db, meeting_id=meeting_id, meeting=meeting)


@router.delete("/{meeting_id}", response_model=meeting_schemas.Meeting)
def delete_meeting(
    meeting_id: int, db: Session = Depends(db.get_db)
) -> meeting_schemas.Meeting:
    return crud.delete_meeting(db=db, meeting_id=meeting_id)


@router.get("/recurrence/", response_model=meeting_recurrence_schemas.MeetingRecurrence)
def get_meeting_recurrence(
    meeting_id: int, db: Session = Depends(db.get_db)
) -> meeting_recurrence_schemas.MeetingRecurrence:
    recurrence = crud.get_meeting_recurrence(db=db, meeting_id=meeting_id)
    if recurrence is None:
        raise HTTPException(status_code=404, detail="Recurrence not found")
    return recurrence


@router.get("/next_occurrence/", response_model=meeting_schemas.Meeting)
def get_next_occurrence(
    meeting_id: int, db: Session = Depends(db.get_db)
) -> meeting_schemas.Meeting:
    next_occurrence = crud.get_next_occurrence(db=db, meeting_id=meeting_id)
    if next_occurrence is None:
        raise HTTPException(status_code=404, detail="Next occurrence not found")
    return next_occurrence


@router.post("/{meeting_id}/complete/", response_model=meeting_schemas.Meeting)
def complete_meeting(
    meeting_id: int, db: Session = Depends(db.get_db)
) -> meeting_schemas.Meeting:
    crud.complete_meeting(db=db, meeting_id=meeting_id)
    return {"message": "Meeting completed"}


@router.post("/{meeting_id}/add_recurrence/", response_model=meeting_schemas.Meeting)
def add_recurrence(
    meeting_id: int, recurrence_id: int, db: Session = Depends(db.get_db)
) -> meeting_schemas.Meeting:
    meeting = crud.add_recurrence(
        db=db, meeting_id=meeting_id, recurrence_id=recurrence_id
    )
    if meeting is None:
        raise HTTPException(status_code=400, detail="Recurrence ID is required")
    return meeting
