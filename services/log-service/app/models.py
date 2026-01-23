from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from .database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    level = Column(String, index=True)
    service_name = Column(String, index=True)
    message = Column(String)
