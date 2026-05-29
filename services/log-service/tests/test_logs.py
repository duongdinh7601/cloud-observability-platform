from app.models import Log

def test_get_logs_empty(client, testing_session_local):
    with testing_session_local() as db:
        db.query(Log).delete()
        db.commit()
        
    response = client.get("/logs")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "next_cursor" in data
    
    assert isinstance(data["items"], list)
    assert data["items"] == []

    assert data["next_cursor"] is None


def test_cursor_pagination_two_logs(client, testing_session_local):
    # Clean table
    with testing_session_local() as db:
        db.query(Log).delete()
        db.commit()

    # Create two logs
    log1 = {
        "timestamp": "2026-01-01T00:00:02Z",
        "level": "INFO",
        "service_name": "auth",
        "message": "second",
    }
    log2 = {
        "timestamp": "2026-01-01T00:00:01Z",
        "level": "INFO",
        "service_name": "auth",
        "message": "first",
    }

    r1 = client.post("/logs", json=log1)
    r2 = client.post("/logs", json=log2)

    # First page
    page1 = client.get("/logs", params={"limit": 1})
    data1 = page1.json()

    # Extract cursor
    cursor = data1["next_cursor"]

    # Second page using cursor
    page2 = client.get("/logs", params={
        "limit": 1,
        "cursor_ts": cursor["cursor_ts"],
        "cursor_id": cursor["cursor_id"],
    })
    data2 = page2.json()

    assert len(data1["items"]) == 1
    assert len(data2["items"]) == 1

    assert data1["items"][0]["message"] == "second"
    assert data2["items"][0]["message"] == "first"

    id_page1 = data1["items"][0]["id"]
    id_page2 = data2["items"][0]["id"]

    assert id_page1 != id_page2


def test_log_with_metadata(client, testing_session_local):
    with testing_session_local() as db:
        db.query(Log).delete()
        db.commit()

    metadata = {
        "request_id": "req-123",
        "duration_ms": 67,
    }
    log_with_metadata = {
        "timestamp": "2026-01-01T00:00:02Z",
        "level": "INFO",
        "service_name": "auth",
        "message": "has metadata",
        "metadata": metadata,
    }

    create_response = client.post("/logs", json=log_with_metadata)
    assert create_response.status_code == 201
    assert create_response.json()["metadata"] == metadata

    list_response = client.get("/logs")
    assert list_response.status_code == 200
    assert list_response.json()["items"][0]["metadata"] == metadata
