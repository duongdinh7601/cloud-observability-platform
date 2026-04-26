# Log Service

The Log Service is a FastAPI microservice responsible for ingesting, storing, and retrieving logs for the Cloud Observability Platform.

It is designed as an internal backend service that can be run locally, tested in isolation, and deployed as part of a multi-service container stack.

## Responsibilities

- Accept log entries through `POST /logs`
- Return logs through `GET /logs`
- Support cursor pagination, filtering, and stable newest-first ordering
- Expose operational health endpoints for container readiness and liveness

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic v2
- SQLAlchemy 2.x
- PostgreSQL
- psycopg v3
- pytest

## API Surface

- `POST /logs`
- `GET /logs`
- `GET /health/live`
- `GET /health/ready`

## Key Behaviors

### Pagination

- Uses a cursor composed of `(timestamp, id)`
- Orders by `timestamp DESC, id DESC`
- Avoids offset-based pagination drift under concurrent writes

### Filtering

- `level`
- `service_name`
- `start_time`
- `end_time`

### Operational Design

- Readiness checks confirm the service can still reach PostgreSQL
- Liveness stays lightweight and process-focused
- CORS is only enabled when origins are explicitly configured

## Local Development

1. Move into the service directory:
```bash
cd services/log-service
```
2. Create and activate a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Copy local environment defaults:
```bash
copy .env.example .env
```
5. Start the API:
```bash
uvicorn app.main:app --reload
```

## Configuration

Local development reads values from `.env`.

Important settings:

- `DATABASE_URL`
- `TEST_DATABASE_URL`
- `CORS_ORIGINS`

When `DATABASE_URL` is omitted for local-only usage, the service falls back to the default defined in `app/settings.py`.

## Testing

Run the integration tests with:

```bash
pytest
```

The test suite uses a dedicated test database and dependency overrides so API behavior can be verified without touching the development database.

## Service Structure

```text
services/log-service/
|-- app/
|   |-- health.py
|   |-- main.py
|   |-- models.py
|   |-- routes.py
|   |-- schemas.py
|   |-- settings.py
|-- scripts/
|   |-- container_healthcheck.py
|-- tests/
|   |-- test_logs.py
|-- Dockerfile
|-- requirements.txt
|-- .env.example
|-- README.md
```
