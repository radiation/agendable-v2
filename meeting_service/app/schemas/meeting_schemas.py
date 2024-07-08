from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MeetingRecurrenceBase(BaseModel):
    frequency: str
    week_day: Optional[int]
    month_week: Optional[int]
    interval: int
    end_recurrence: Optional[datetime]


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


class Meeting(MeetingBase):
    id: int
    recurrence: Optional[MeetingRecurrenceBase]

    class Config:
        orm_mode = True
