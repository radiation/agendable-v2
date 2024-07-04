from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRecurrenceBase(BaseModel):
    # Define fields for MeetingRecurrence
    pass


class MeetingRecurrence(MeetingRecurrenceBase):
    id: int

    class Config:
        orm_mode = True


class MeetingBase(BaseModel):
    title: str = Field(default="", max_length=100)
    start_date: datetime
    end_date: datetime
    duration: int = Field(default=30)
    location: str = Field(default="", max_length=100)
    notes: str = Field(default="")
    num_reschedules: int = Field(default=0)
    reminder_sent: bool = Field(default=False)

    @validator("end_date")
    def end_date_must_be_after_start_date(cls, v, values, **kwargs):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("End date must be after start date")
        return v


class MeetingCreate(MeetingBase):
    recurrence_id: Optional[int]


class MeetingUpdate(MeetingBase):
    pass


class MeetingInDBBase(MeetingBase):
    id: int
    created_at: datetime
    recurrence: Optional[MeetingRecurrence]

    class Config:
        orm_mode = True


class Meeting(MeetingInDBBase):
    recurrence_id: Optional[int]
    recurrence: Optional[MeetingRecurrence]


class MeetingRecurrenceCreate(MeetingRecurrenceBase):
    pass


class MeetingRecurrenceUpdate(MeetingRecurrenceBase):
    pass
