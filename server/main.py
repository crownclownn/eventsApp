from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import uvicorn


app = FastAPI()


class Event(BaseModel):
    name: str
    date: str
    time: str
    location: str
    user_email: str

@app.on_event("startup")
async def startup():
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, name TEXT, date TEXT, time TEXT, location TEXT, user_email TEXT)"
    )
    conn.commit()
    conn.close()

@app.post("/events")
async def create_event(event: Event):
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO events (name, date, time, location, user_email) VALUES (?, ?, ?, ?, ?)",
        (event.name, event.date, event.time, event.location, event.user_email),
    )
    conn.commit()
    conn.close()

@app.get("/events")
async def read_events():
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    events = c.fetchall()
    conn.close()
    return events

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)