import sqlalchemy.sql.functions as func
from sqlalchemy import Column, DateTime, ForeignKey, Integer

from . import Base


class MeetingTask(Base):
    __tablename__ = "meeting_tasks"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
