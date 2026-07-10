from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from app.database import get_db
from app.main import app
from app.settings import TEST_DATABASE_URL
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

assert TEST_DATABASE_URL, "TEST_DATABASE_URL is not set"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def ensure_test_database_url():
    if "test" not in TEST_DATABASE_URL:
        raise RuntimeError("Refusing to reset a non-test database")


def reset_test_database():
    ensure_test_database_url()

    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS logs CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))


# Run Alembic migrations against the test database before tests use it
def run_migrations():
    service_root = Path(__file__).resolve().parents[1]
    alembic_cfg = Config(str(service_root / "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def prepare_test_database():
    reset_test_database()
    run_migrations()


@pytest.fixture
def testing_session_local():
    return TestingSessionLocal


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
