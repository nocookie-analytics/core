from app.models.event import EventType
from typing import Dict, Optional

from pydantic import BaseModel


# Shared properties
class EventBase(BaseModel):
    domain_id: Optional[int] = None


# Properties to receive on item creation
class EventCreate(EventBase):
    domain_id: int
    uid: str
    event_type: EventType
    ua_string: str
    path: str
    url_params: Dict
    page_title: str
    status_code: int
    load_time_ms: int
    page_size_bytes: int
    referrer: str
    user_timezone: str


# Properties shared by models stored in DB
class EventInDBBase(EventBase):
    id: int
    domain_name: str
    owner_id: int

    class Config:
        orm_mode = True
