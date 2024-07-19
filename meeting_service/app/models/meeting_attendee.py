import sqlalchemy.sql.functions as func
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer

from . import Base


class MeetingAttendee(Base):
    __tablename__ = "meeting_attendees"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    user_id = Column(Integer)
    is_scheduler = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
