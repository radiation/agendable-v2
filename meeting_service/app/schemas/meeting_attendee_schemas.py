from pydantic import BaseModel, ConfigDict


class MeetingAttendeeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    meeting_id: int
    task_id: int


class MeetingAttendeeCreate(MeetingAttendeeBase):
    pass


class MeetingAttendeeUpdate(MeetingAttendeeBase):
    pass


class MeetingAttendee(MeetingAttendeeBase):
    id: int
