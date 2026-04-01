# Log Service

The Log Service is a **backend microservice** in the Cloud Observability Platform.  
It is responsible for ingesting, storing, and retrieving application logs in a scalable and production-oriented way.

This service exposes a REST API consumed by the frontend dashboard and is designed to be modular, independently deployable, and horizontally scalable.

---

## Responsibilities

- Accept log entries via HTTP (`POST /logs`)  
- Store logs in PostgreSQL  
- Provide **filtered and cursor-paginated** access to logs (`GET /logs`)  
- Enforce input validation and API contracts
- Serve as a standalone microservice suitable for containerized deployment 

---

## Tech Stack

- **Python + FastAPI** - API backend
- **Pydantic v2** - request/response validation
- **SQLAlchemy** - ORM  
- **PostgreSQL** - persistent log storage
- **psycopg** - Postgres driver
- **pytest** - integration testing
- **Uvicorn** - ASGI server  
- **Docker** - containerization  

---

## Key Features

**Cursor-Based Pagination**
- Pagination uses a cursor composed of `(timestamp, id)`
- Prevents performance issues and inconsistencies caused by offset-based pagination
- Ensures:
  - no duplicate results
  - stable ordering under concurrent writes
 
**Filtering**
- Filter logs by:
  - log level
  - service name (case-insensitive)
  - time range(`start_time`, `end_time`)
- Input validation handled via FastAPI dependencies

**Testing**
- Integration tests using **pytest**
- Separate **PostgreSQL test database**
- FastAPI dependency overrides for clean test isolation
- Deterministic, repeatable test runs

---

## Folder Structure

log-service/
```graphql
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── database.py      # SQLAlchemy engine + session
│   ├── models.py        # ORM models
│   ├── routes.py        # API routes
│   ├── schemas.py       # Pydantic schemas
│   └── dependencies.py  # Request parsing & validation dependencies
│
├── tests/
│   └── test_logs.py     # Integration tests
│
├── requirements.txt     # Python dependencies
├── .env                 # Local environment variables (gitignored)
├── Dockerfile           # Container build (Phase 3)
└── README.md
```

--- 

## Setup Instructions

1. Navigate to the log-service folder:  
```bash
cd services/log-service
```
2. Create and activate a virtual environment:
```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Configure environment variables:
```bash
copy .env.example .env
```
Then update values as needed for your local PostgreSQL setup:
```bash
DATABASE_URL=postgresql+psycopg://log_user:logpw@localhost:5432/log_service_db
TEST_DATABASE_URL=postgresql+psycopg://log_user:logpw@localhost:5432/log_service_test_db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```
5. Start the service locally:
```bash
uvicorn app.main:app --reload
```
The service will run on `http://localhost:8000` (or your chosen port)
If `DATABASE_URL` is omitted locally, the app falls back to the same default shown above for convenience.
Docker Compose uses the env values defined in the repo root `docker-compose.yml`.

---

## API Endpoints

- `POST /logs` -> Create a new log entry
- `GET /logs`
  - Retrieve logs with:
    - cursor-based pagination
    - optional filters
    - stable ordering (newest first)
  - Response includes:
    - `items`: list of log entries
    - `next_cursor`: cursor for fetching the next page

For full API documentation, see `docs/log-service.md`

---

## Testing

Run integration tests:
```bash
pytest
```

Tests:
- use a dedicated test database
- override database dependencies
- validate cursor pagination behavior end-to-end

---

## Notes

- The service is stateless and safe to scale horizontally
- Database access is abstracted via dependency injection
- Pagination strategy matches real-world production systems
- Environment-based configuration enables Docker and CI/CD workflows


