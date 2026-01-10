# Log Service

The Log Service is the first backend service in the Cloud Observability Platform. It handles ingestion, storage, and retrieval of log entries.

---

## Responsibilities

- Accept log entries via HTTP (`POST /logs`)
- Store logs in PostgreSQL
- Allow querying of logs (`GET /logs`) with filters
- Provide paginated results
- Serve as a backend API for the frontend dashboard

---

## Data Model (Conceptual)

**LogEntry Table**

| Field         | Type        | Description                        |
|---------------|------------|------------------------------------|
| id            | UUID       | Unique identifier for the log      |
| timestamp     | datetime   | When the log was created           |
| level         | string     | Log severity (INFO, WARN, ERROR)  |
| service_name  | string     | Name of the service generating log |
| message       | text       | Log message content                |

---

## API Endpoints (Conceptual)

### `POST /logs`

**Purpose:** Accept a log entry

**Request Body Example:**
```json
{
  "timestamp": "2026-01-09T18:00:00Z",
  "level": "ERROR",
  "service_name": "frontend",
  "message": "Failed to fetch logs"
}
