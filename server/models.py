from pydantic import BaseModel

class Event(BaseModel):
    name: str
    date: str
    time: str
    location: str
    user_email: str
