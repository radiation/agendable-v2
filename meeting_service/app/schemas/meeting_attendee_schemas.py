from typing import Optional

from pydantic import BaseModel, ConfigDict


class MeetingAttendeeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    meeting_id: int
    user_id: int
    is_scheduler: Optional[bool] = False


class MeetingAttendeeCreate(MeetingAttendeeBase):
    pass


class MeetingAttendeeUpdate(MeetingAttendeeBase):
    pass


class MeetingAttendee(MeetingAttendeeBase):
    id: int
