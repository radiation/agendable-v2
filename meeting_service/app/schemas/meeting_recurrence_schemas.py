import datetime

from dateutil.rrule import rrulestr
from pydantic import BaseModel, field_validator


# Define a base class that will be used to create other classes.
class MeetingRecurrenceBase(BaseModel):
    rrule: str


class MeetingRecurrenceCreate(MeetingRecurrenceBase):
    @field_validator("rrule")
    def validate_rrule(cls, value):
        try:
            # Attempt to parse the rule to ensure its validity
            rrulestr(value, dtstart=datetime.datetime.now())
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid recurrence rule: {str(e)}")
        return value


class MeetingRecurrenceUpdate(MeetingRecurrenceBase):
    pass


class MeetingRecurrence(MeetingRecurrenceCreate):
    id: int

    class Config:
        orm_mode = True
