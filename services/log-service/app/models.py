from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from .database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    # Use timezone-aware timestamps so logs from different systems can be compared safely.
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    # These fields are indexed because they are used frequently in filtering and ordering.
    level = Column(String, index=True)
    service_name = Column(String, index=True)
    message = Column(String)
    log_metadata = Column("metadata", JSONB, nullable=True)
