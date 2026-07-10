from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from app.schemas import LogLevel


def parse_level(level: Optional[str] = None) -> Optional[LogLevel]:
    if level is None:
        return None

    normalized = level.strip().upper()

    if normalized == "WARN":
        normalized = "WARNING"

    try:
        return LogLevel[normalized]
    except KeyError:
        allowed = ", ".join(e.value for e in LogLevel)
        raise HTTPException(
            status_code=422, detail=f"Invalid level '{level}'. Allowed: {allowed}"
        ) from None


def resolve_cursor(
    cursor_ts: Optional[datetime] = None, cursor_id: Optional[int] = None
):
    if cursor_ts is not None and cursor_id is not None:
        return (cursor_ts, cursor_id)
    elif cursor_ts is None and cursor_id is None:
        return None
    else:
        raise HTTPException(
            status_code=422, detail="Both cursor_ts and cursor_id are required"
        )
