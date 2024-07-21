from datetime import datetime
from typing import Optional

from app.schemas.meeting_recurrence_schemas import MeetingRecurrence
from pydantic import BaseModel


class MeetingBase(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime
    duration: int
    location: str
    notes: str
    num_reschedules: int
    reminder_sent: bool


class MeetingCreate(MeetingBase):
    pass


class MeetingUpdate(MeetingBase):
    pass


class Meeting(MeetingBase):
    id: int
    recurrence: Optional[MeetingRecurrence]

    class Config:
        orm_mode = True
