from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(tags=["health"])


def is_alive() -> bool:
    # Liveness only answers "is the process up?" so it stays lightweight.
    return True


def is_ready(db: Session) -> bool:
    # Readiness is stricter: the service should only accept traffic if it can still
    # reach its dependencies, which is the database for this service.
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


@router.get("/live", summary="Liveness check")
def liveness_check():
    if not is_alive():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_live"},
        )
    return {"status": "ok"}


@router.get("/ready", summary="Readiness check")
def readiness_check(db: Session = Depends(get_db)):
    # FastAPI injects a request-scoped DB session so readiness reflects real DB access.
    if not is_ready(db):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready"},
        )
    return {"status": "ok"}
