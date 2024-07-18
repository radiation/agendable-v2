import sqlalchemy.sql.functions as func
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


"""
Store the RFC 5545 recurrence rule string
rrules aren't TZ aware so these will always be UTC

Examples:
FREQ=WEEKLY;BYDAY=TU;BYHOUR=17;BYMINUTE=30
FREQ=MONTHLY;BYMONTHDAY=15;BYHOUR=9;BYMINUTE=0
FREQ=YEARLY;BYMONTH=6;BYMONTHDAY=24;BYHOUR=12;BYMINUTE=0
"""


class MeetingRecurrence(Base):
    __tablename__ = "meeting_recurrences"

    id = Column(Integer, primary_key=True)
    rrule = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<MeetingRecurrence(rrule={self.rrule})>"


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True)
    recurrence_id = Column(Integer, ForeignKey("meeting_recurrences.id"), nullable=True)
    title = Column(String(100), default="")
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    duration = Column(Integer, default=30)
    location = Column(String(100), default="")
    notes = Column(String)
    num_reschedules = Column(Integer, default=0)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    recurrence = relationship("MeetingRecurrence", back_populates="meetings")


MeetingRecurrence.meetings = relationship("Meeting", back_populates="recurrence")


class MeetingAttendee(Base):
    __tablename__ = "meeting_attendees"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    user_id = Column(Integer)
    is_scheduler = Column(Boolean, default=False)


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


class MeetingTask(Base):
    __tablename__ = "meeting_tasks"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
