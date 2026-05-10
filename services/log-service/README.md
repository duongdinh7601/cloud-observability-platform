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
- Alembic
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
- Kubernetes injects `DATABASE_URL` from a Secret and routes traffic through an internal ClusterIP Service

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

## Database Migrations

The service uses Alembic to manage database schema changes. The FastAPI app does not create tables automatically on startup; schema changes should be applied intentionally through migrations.

Run migration commands from the service directory:

```bash
cd services/log-service
```

Apply all pending migrations:

```bash
alembic upgrade head
```

Create a new migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe schema change"
```

Review generated migration files before applying them. Autogeneration is a starting point, not a substitute for understanding the schema change.

## Testing

Run the integration tests with:

```bash
pytest
```

The test suite uses a dedicated test database and dependency overrides so API behavior can be verified without touching the development database.

## Local Kubernetes

From the repo root, build the local Kubernetes image and apply the dev overlay:

```bash
docker build -t log-service:k8s-dev services/log-service
kubectl apply -k infra/kubernetes/overlays/dev
```

The service is internal to the cluster. For local Swagger UI access, use:

```bash
kubectl port-forward service/log-service 8000:8000
```

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
|-- alembic/
|   |-- versions/
|-- scripts/
|   |-- container_healthcheck.py
|-- tests/
|   |-- test_logs.py
|-- Dockerfile
|-- alembic.ini
|-- requirements.txt
|-- .env.example
|-- README.md
```
