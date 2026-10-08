from datetime import datetime

from pydantic import BaseModel, field_validator


class Event(BaseModel):
    event_id: str
    user_id: str
    event_type: str
    timestamp: datetime
    source: str

    @field_validator("event_id", "user_id", "event_type", "source")
    @classmethod
    def normalize_text(cls, value):
        value = value.strip().lower()

        if not value:
            raise ValueError("Field cannot be empty")

        return value