from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    due_date: Optional[datetime]
    completed: bool
    completed_date: Optional[datetime]


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    assignee_id: int

    class Config:
        orm_mode = True


class TaskResponse(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
