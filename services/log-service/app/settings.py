import os
from pathlib import Path

from dotenv import load_dotenv


SERVICE_ROOT = Path(__file__).resolve().parent.parent
# Centralize config loading here so env values are available before modules like
# app.database read them at import time.
load_dotenv(SERVICE_ROOT / ".env")


def _split_csv(value: str) -> list[str]:
    # CORS origins are stored as a comma-separated env var and normalized into a list.
    return [item.strip() for item in value.split(",") if item.strip()]


# Local development can fall back to a default database URL until deployment config is enforced.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://log_user:logpw@localhost:5432/log_service_db",
)
CORS_ORIGINS = _split_csv(os.getenv("CORS_ORIGINS", ""))
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
