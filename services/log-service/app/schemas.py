from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


class LogEntry(BaseModel):
    timestamp: datetime
    level: LogLevel
    service_name: str
    message: str
    metadata: Optional[dict] = None


class LogResponse(BaseModel):
    id: int
    timestamp: datetime
    level: LogLevel
    service_name: str
    message: str
    metadata: Optional[dict] = Field(default=None, validation_alias="log_metadata")

    model_config = ConfigDict(from_attributes=True)


class CursorResponse(BaseModel):
    cursor_ts: datetime
    cursor_id: int


class LogListResponse(BaseModel):
    items: List[LogResponse]
    next_cursor: Optional[CursorResponse] = None
