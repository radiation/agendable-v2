from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    recurrence_id = Column(Integer, ForeignKey("meeting_recurrences.id"), nullable=True)
    title = Column(String(100), default="")
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    duration = Column(Integer, default=30)
    location = Column(String(100), default="")
    notes = Column(Text, default="")
    num_reschedules = Column(Integer, default=0)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    recurrence = relationship("MeetingRecurrence", back_populates="meetings")


class MeetingRecurrence(Base):
    __tablename__ = "meeting_recurrences"

    id = Column(Integer, primary_key=True, index=True)
    meetings = relationship("Meeting", back_populates="recurrence")
