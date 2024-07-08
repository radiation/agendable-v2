from pydantic import BaseModel


class MeetingTaskBase(BaseModel):
    meeting_id: int
    task_id: int


class MeetingTaskCreate(MeetingTaskBase):
    pass


class MeetingTask(MeetingTaskBase):
    id: int

    class Config:
        orm_mode = True
