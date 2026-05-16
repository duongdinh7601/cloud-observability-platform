from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

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
    
    class Config:
        from_attributes = True

class CursorResponse(BaseModel):
    cursor_ts: datetime
    cursor_id: int

class LogListResponse(BaseModel):
    items: List[LogResponse]
    next_cursor: Optional[CursorResponse]=None