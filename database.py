# database.py
import sqlite3
from datetime import datetime

DB_FILE = "incidents.db"

def init_db():
    """Creates the incidents table if it does not exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                title TEXT NOT NULL,
                sanitized_alert TEXT NOT NULL,
                status TEXT NOT NULL,
                diagnosis TEXT,
                proposed_fix TEXT
            )
        """)
        conn.commit()

def save_incident(sanitized_alert: str, status: str, diagnosis: str, proposed_fix: str) -> int:
    """Saves a processed incident and returns its database ID."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Truncate alert for a clean sidebar title (e.g., "Kubernetes alert: auth-service...")
    title = sanitized_alert[:40] + ("..." if len(sanitized_alert) > 40 else "")
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO incidents (timestamp, title, sanitized_alert, status, diagnosis, proposed_fix)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, title, sanitized_alert, status, diagnosis, proposed_fix))
        conn.commit()
        return cursor.lastrowid

def get_all_incidents():
    """Returns the history list for the sidebar."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, title, status FROM incidents ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_incident_by_id(incident_id: int):
    """Retrieves full details when a user clicks a history item."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,))
        row = cursor.fetchone()
        return dict(row) if row else None