import sqlalchemy.sql.functions as func
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from . import Base

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
    title = Column(String(100), default="")
    rrule = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Define the relationship here
    meetings = relationship("Meeting", back_populates="recurrence")

    def __repr__(self):
        return f"<MeetingRecurrence(title={self.title}, rrule={self.rrule})>"
