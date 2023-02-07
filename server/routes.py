import sqlite3
from fastapi import FastAPI
from .models import Event
from .main import app

@app.post("/events")
async def create_event(event: Event):
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute("INSERT INTO events (name, date, time, location, user_email) VALUES (?, ?, ?, ?, ?)", 
              (event.name, event.date, event.time, event.location, event.user_email))
    conn.commit()
    conn.close()
    return {"message": "Event created successfully"}

@app.get("/events")
async def read_events():
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    events = [{"name": row[0], "date": row[1], "time": row[2], "location": row[3], "user_email": row[4]} for row in c.fetchall()]
    conn.close()
    return events
