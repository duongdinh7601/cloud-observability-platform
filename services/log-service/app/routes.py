from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Log
from app.schemas import LogEntry, LogListResponse, LogLevel, CursorResponse
from app.dependencies import parse_level, resolve_cursor
from typing import Optional, Tuple
from datetime import datetime

router = APIRouter()

@router.post("/logs", status_code=201)
def create_log(log: LogEntry, db: Session = Depends(get_db)):
    db_log = Log(
        timestamp=log.timestamp,
        level=log.level,
        service_name=log.service_name,
        message=log.message,
    )

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return db_log

@router.get("/logs", response_model=LogListResponse)
def get_logs(
    limit: int= Query(50, ge=1, le=200), 
    cursor: Optional[Tuple[datetime, int]] = Depends(resolve_cursor),
    level: Optional[LogLevel]= Depends(parse_level), 
    service_name: Optional[str]=None,
    start_time: Optional[datetime]=None,
    end_time: Optional[datetime]=None,
    db: Session = Depends(get_db)
    ):

    query = db.query(Log).order_by(Log.timestamp.desc(), Log.id.desc())

    if level is not None:
        query = query.filter(Log.level == level)
    
    if service_name is not None:
        normalized_service = service_name.strip().lower()
        if normalized_service:
            query = query.filter(func.lower(Log.service_name) == normalized_service)

    if start_time is not None and end_time is not None:
        if start_time > end_time:
            raise HTTPException(
                status_code=422,
                detail="start_time must be <= end_time"
                )
    
    if start_time is not None:
        query = query.filter(Log.timestamp >= start_time)

    if end_time is not None:
        query = query.filter(Log.timestamp <= end_time)

    if cursor is not None:
        cursor_ts, cursor_id = cursor
        query =query.filter(
            or_(Log.timestamp < cursor_ts, and_(Log.timestamp == cursor_ts, Log.id < cursor_id))
        )

    query = query.limit(limit)
    logs = query.all()

    if not logs:
        next_cursor = None
    else:
        last_log = logs[-1]
        next_cursor = CursorResponse(cursor_ts=(last_log.timestamp), cursor_id=last_log.id)
    
    return LogListResponse(items=logs, next_cursor=next_cursor)