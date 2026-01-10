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

**Description:** Create a new log entry.

**HTTP Method:** `POST`  
**URL:** `/logs`

**Request Body Example:**
```json
{
  "timestamp": "2026-01-09T18:00:00Z",
  "level": "ERROR",
  "service_name": "frontend",
  "message": "Failed to fetch logs"
}
```
**Response Codes:**

- 201 - Log entry created successfully
- 400 - Invlid request body
- 500 - Internal server error

**Notes:**
- The service validates all firlds brfore inserting into the database
- Timestamps must be ISO 8601 formatted

---

### `GET /logs`

**Description:** Retrieve log entries with optional filters and pagination.

**HTTP Method:** `GET`  
**URL:** `/logs`

**Query Parameters:**

| Field         | Type   | Description                        
|---------------|-------|------------------------------------
| `start_time`  | string | ISO 8601 timestamp for the earliest log to include
| `end_time`    | string | ISO 8601 timestamp for the latest log to include
| `level`       | string | Filter by log severity (`INFO`, `WARN`, `ERROR`) 
| `service_name`| string | Filter by the service generating logs 
| `page`        | integer | Page number for paginated results (default: 1)
| `limit`       | integer | Number of results per page (default: 50)

**Request Example:**
```pgsql
GET /logs?start_time=2026-01-09T00:00:00Z&end_time=2026-01-09T23:59:59Z&level=ERROR&page=1&limit=20
```

**Response Example (200 OK):**
```json
{
  "page": 1,
  "limit": 20,
  "total": 42,
  "logs": [
    {
      "id": "uuid-123",
      "timestamp": "2026-01-09T18:00:00Z",
      "level": "ERROR",
      "service_name": "frontend",
      "message": "Failed to fetch logs"
    },
    {
      "id": "uuid-124",
      "timestamp": "2026-01-09T18:05:00Z",
      "level": "ERROR",
      "service_name": "api-gateway",
      "message": "Timeout connecting to Log Service"
    }
  ]
}
```

**Response Codes:**

- 200 - Logs retrieved successfully
- 400 - Invlid query parameters
- 500 - Internal server error

**Notes:**
- Pagination is optional; defaults to `page=1` and `limit=50`
- Filters (`start_time`, `end_time`, `level`, `service_name`) are optional
- `total` indicates the number of logs matching the filter criteria
