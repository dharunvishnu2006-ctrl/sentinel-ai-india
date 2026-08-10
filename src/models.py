from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class Task(BaseModel):
    id: int
    urgency: int = Field(ge=1, le=5)
    name: str
    created_at: datetime


class Event(BaseModel):
    agent: str
    kind: Literal["info", "warning", "error"]
    payload: str
    at: datetime
