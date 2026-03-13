# health.py contains all the operational endpoints that make sure the backend service is live and ready

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(tags=["health"])

# helper functions to check if service is live/ready
def is_alive() -> bool:
    return True

def is_ready(db: Session) -> bool:
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False

# route definitions with route handlers
@router.get("/live", summary="Liveness check")
def liveness_check():
    if not is_alive():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_live"}
        )
    return {"status": "ok"}

@router.get("/ready", summary="Readiness check")
def readiness_check(db: Session = Depends(get_db)):
    if not is_ready(db):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready"}
        )
    return {"status": "ok"}