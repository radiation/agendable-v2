from pydantic import BaseModel


class MeetingAttendeeBase(BaseModel):
    meeting_id: int
    task_id: int


class MeetingAttendeeCreate(MeetingAttendeeBase):
    pass


class MeetingAttendee(MeetingAttendeeBase):
    id: int

    class Config:
        orm_mode = True
