import sqlalchemy.sql.functions as func
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, event
from sqlalchemy.orm import relationship

from . import Base


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
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    recurrence = relationship("MeetingRecurrence", back_populates="meetings")


@event.listens_for(Meeting, "before_insert")
@event.listens_for(Meeting, "before_update")
def receive_before_save(mapper, connection, target):
    # Set the title based on recurrence if the title is empty
    if not target.title and target.recurrence:
        target.title = (
            f"{target.recurrence.title} on {target.start_date.strftime('%Y-%m-%d')}"
        )
