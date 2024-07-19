import sqlalchemy.sql.functions as func
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from . import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    assignee_id = Column(Integer)
    title = Column(String(100), default="")
    description = Column(String(1000), default="")
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed = Column(Boolean, default=False)
    completed_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
