import datetime

from dateutil.rrule import rrulestr
from pydantic import BaseModel, field_validator


class MeetingRecurrenceCreate(BaseModel):
    rrule: str

    @field_validator("rrule")
    def validate_rrule(cls, value):
        try:
            # Attempt to parse the rule to ensure its validity
            rrulestr(value, dtstart=datetime.datetime.now())
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid recurrence rule: {str(e)}")
        return value


class MeetingRecurrence(MeetingRecurrenceCreate):
    id: int

    class Config:
        orm_mode = True
