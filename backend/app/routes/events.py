from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import get_connection

router = APIRouter()

class EventCreate(BaseModel):
    title: str
    date: str
    venue: str
    capacity: int

@router.post("/events", status_code=201)
def create_event(event: EventCreate):
    if event.capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be greater than zero")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO events (title, date, venue, capacity) VALUES (?, ?, ?, ?)",
        (event.title, event.date, event.venue, event.capacity)
    )
    conn.commit()
    event_id = cur.lastrowid
    conn.close()
    return {"id": event_id, "message": "Event created successfully"}

@router.get("/events")
def list_events():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r["id"], "title": r["title"], "date": r["date"],
             "venue": r["venue"], "capacity": r["capacity"]} for r in rows]

@router.get("/events/{event_id}")
def get_event(event_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"id": row["id"], "title": row["title"], "date": row["date"],
            "venue": row["venue"], "capacity": row["capacity"]}