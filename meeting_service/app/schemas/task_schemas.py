from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    due_date: Optional[datetime]
    assignee_id: int
    completed: bool
    completed_date: Optional[datetime]


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    assignee_id: int


class TaskResponse(TaskBase):
    id: int
    user_id: int
