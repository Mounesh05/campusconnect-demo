import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db, get_connection
import os

os.environ["TESTING"] = "1"

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield
    conn = get_connection()
    conn.execute("DELETE FROM attendance")
    conn.execute("DELETE FROM registrations")
    conn.execute("DELETE FROM events")
    conn.commit()
    conn.close()

client = TestClient(app)

def test_create_event():
    response = client.post("/api/events", json={
        "title": "AI Workshop",
        "date": "2026-11-15",
        "venue": "Seminar Hall",
        "capacity": 100
    })
    assert response.status_code == 201
    assert "id" in response.json()

def test_list_events():
    client.post("/api/events", json={
        "title": "Tech Talk",
        "date": "2026-11-20",
        "venue": "Lab 1",
        "capacity": 50
    })
    response = client.get("/api/events")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_create_event_invalid_capacity():
    response = client.post("/api/events", json={
        "title": "Bad Event",
        "date": "2026-11-25",
        "venue": "Room 3",
        "capacity": 0
    })
    assert response.status_code == 400

def test_get_event_not_found():
    response = client.get("/api/events/9999")
    assert response.status_code == 404