import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "campusconnect.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            venue TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            participant_name TEXT NOT NULL,
            participant_email TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id),
            UNIQUE (event_id, participant_email)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id INTEGER NOT NULL UNIQUE,
            checked_in_at TEXT NOT NULL,
            FOREIGN KEY (registration_id) REFERENCES registrations(id)
        )
    """)

    conn.commit()
    conn.close()