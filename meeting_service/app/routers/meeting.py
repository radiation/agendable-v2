import crud
import schemas
from db import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/meetings/", response_model=schemas.Meeting)
def create_meeting(meeting: schemas.MeetingCreate, db: Session = Depends(get_db)):
    return crud.create_meeting(db=db, meeting=meeting)


@router.get("/meetings/", response_model=list[schemas.Meeting])
def read_meetings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_meetings(db=db, skip=skip, limit=limit)


@router.get("/meetings/{meeting_id}", response_model=schemas.Meeting)
def read_meeting(meeting_id: int, db: Session = Depends(get_db)):
    db_meeting = crud.get_meeting(db=db, meeting_id=meeting_id)
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return db_meeting


@router.put("/meetings/{meeting_id}", response_model=schemas.Meeting)
def update_meeting(
    meeting_id: int, meeting: schemas.MeetingUpdate, db: Session = Depends(get_db)
):
    return crud.update_meeting(db=db, meeting_id=meeting_id, meeting=meeting)


@router.delete("/meetings/{meeting_id}", response_model=schemas.Meeting)
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    return crud.delete_meeting(db=db, meeting_id=meeting_id)


@router.get("/meetings/recurrence/", response_model=schemas.MeetingRecurrence)
def get_meeting_recurrence(meeting_id: int, db: Session = Depends(get_db)):
    recurrence = crud.get_meeting_recurrence(db=db, meeting_id=meeting_id)
    if recurrence is None:
        raise HTTPException(status_code=404, detail="Recurrence not found")
    return recurrence


@router.get("/meetings/next_occurrence/", response_model=schemas.Meeting)
def get_next_occurrence(meeting_id: int, db: Session = Depends(get_db)):
    next_occurrence = crud.get_next_occurrence(db=db, meeting_id=meeting_id)
    if next_occurrence is None:
        raise HTTPException(status_code=404, detail="Next occurrence not found")
    return next_occurrence


@router.post("/meetings/{meeting_id}/complete/", response_model=schemas.Meeting)
def complete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    crud.complete_meeting(db=db, meeting_id=meeting_id)
    return {"message": "Meeting completed"}


@router.post("/meetings/{meeting_id}/add_recurrence/", response_model=schemas.Meeting)
def add_recurrence(meeting_id: int, recurrence_id: int, db: Session = Depends(get_db)):
    meeting = crud.add_recurrence(
        db=db, meeting_id=meeting_id, recurrence_id=recurrence_id
    )
    if meeting is None:
        raise HTTPException(status_code=400, detail="Recurrence ID is required")
    return meeting
