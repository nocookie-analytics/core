from __future__ import annotations
from furl import furl
from fastapi.exceptions import HTTPException
import pydantic
from app.models.event import EventType
from typing import Dict, Optional

from pydantic import BaseModel


# Shared properties
class EventBase(BaseModel):
    pass


class EventCreated(BaseModel):
    success: bool = True
    error: Optional[str] = None


# Properties to receive on item creation
class EventCreate(EventBase):
    event_type: EventType
    ua_string: str
    path: str
    url_params: Dict
    page_title: str
    page_size_bytes: int
    referrer: Optional[str]
    status_code: Optional[int]  # Not possible in current API
    user_timezone: Optional[str]

    dnslookup_time: Optional[int]
    download_time: Optional[int]
    fetch_time: Optional[int]
    time_to_first_byte: Optional[int]
    total_time: Optional[int]

    @classmethod
    def depends(
        cls: EventCreate,
        et: str,
        uas: str,
        url: str,
        pt: str,
        psb: str,
        ltms: Optional[int] = None,
        sc: Optional[int] = None,
        dnslt: Optional[int] = None,
        dt: Optional[int] = None,
        ft: Optional[int] = None,
        ttfb: Optional[int] = None,
        tt: Optional[int] = None,
        ref: Optional[str] = None,
        ut: Optional[str] = None,
    ) -> EventCreate:
        try:
            event_type = EventType(et)
        except ValueError:
            raise HTTPException(status_code=400, detail="Bad event type")
        if event_type != EventType.page_view:
            raise HTTPException(status_code=400, detail="Bad event type")

        furled_url = furl(url)
        path = str(furled_url.path)
        url_params = dict(
            furled_url.args
        )  # TODO: furl.args is multidict, this conversion is lossy

        try:
            return cls(
                event_type=event_type,
                ua_string=uas,
                page_title=pt,
                status_code=sc,
                load_time_ms=ltms,
                page_size_bytes=psb,
                referrer=ref,
                user_timezone=ut,
                path=path,
                url_params=url_params,
                dnslookup_time=dnslt,
                download_time=dt,
                fetch_time=ft,
                time_to_first_byte=ttfb,
                total_time=tt,
            )
        except pydantic.error_wrappers.ValidationError as e:
            # TODO: Return error fields from exception
            raise HTTPException(status_code=400, detail=e.errors())


class EventUpdate(EventBase):
    pass


# Properties shared by models stored in DB
class EventInDBBase(EventBase):
    id: int
    domain_name: str
    owner_id: int

    class Config:
        orm_mode = True
