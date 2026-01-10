# Log Service

The Log Service is a **backend service** in the Cloud Observability Platform.  
It handles ingestion, storage, and retrieval of log entries for the platform. This service provides the API endpoints that the frontend dashboard consumes.

---

## Responsibilities

- Accept log entries via HTTP (`POST /logs`)  
- Store logs in PostgreSQL  
- Provide filtered and paginated access to logs (`GET /logs`)  
- Serve as a modular, independently deployable service  

---

## Tech Stack

- **Python + FastAPI** for the API backend  
- **PostgreSQL** for persistent log storage  
- **Uvicorn** as ASGI server  
- **Docker** for containerization (optional)  

---

## Folder Structure

log-service/

├── app/ # Application source code

│ ├── main.py # Entry point for FastAPI

│ ├── models.py # Database models (SQLAlchemy / Pydantic)

│ ├── routes.py # API routes

│ ├── schemas.py # Pydantic request/response schemas

│ ├── services.py # Business logic and DB interactions

│ └── utils.py # Utility functions (optional)

├── tests/ # Unit and integration tests

├── requirements.txt # Python dependencies

├── Dockerfile # Docker container configuration

└── README.md

--- 

## Setup Instructions

1. Navigate to the log-service folder:  
```bash
cd services/log-service
```
2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Set environment variables (example `.env` file):
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/logs_db
```
5. Start the service locally:
```bash
uvicorn app.main:app --reload
```
The service will run on `http://localhost:8001` (or your chosen port)

---

## API Endpoints

- `POST /logs` -> Create a new log entry
- `GET /logs` -> Retrieve logs with optional filters and pagination

For full API documentation, see `docs/log-service.md`

---

## Notes

- This service is **modular** and can be scaled independently
- Designed for **containerization and Kubernetes deployment**
- Includes **unit tests and integration tests** for future CI/CD integration
