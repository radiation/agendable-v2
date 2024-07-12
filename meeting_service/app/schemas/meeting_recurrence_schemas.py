from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MeetingRecurrenceBase(BaseModel):
    frequency: str
    week_day: Optional[int]
    month_week: Optional[int]
    interval: int
    end_recurrence: Optional[datetime]


class MeetingRecurrenceCreate(MeetingRecurrenceBase):
    pass


class MeetingRecurrence(MeetingRecurrenceBase):
    id: int

    class Config:
        orm_mode = True
