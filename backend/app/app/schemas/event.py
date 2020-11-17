from __future__ import annotations

from decimal import Decimal
from typing import Dict, Optional

import pydantic
from fastapi.exceptions import HTTPException
from furl import furl
from pydantic import BaseModel, validator
from pydantic.networks import IPvAnyAddress
from starlette.requests import Request

from app.models.event import EventType
from app.models.parsed_ua import ParsedUA


# Shared properties
class EventBase(BaseModel):
    pass


class EventCreated(BaseModel):
    success: bool = True
    error: Optional[str] = None


# Properties to receive on item creation
class EventCreate(EventBase):
    class Config:
        extra = "forbid"

    event_type: EventType
    ua_string: str
    path: str
    url: str
    url_params: Dict
    page_title: str
    page_size_bytes: int
    referrer: Optional[str]
    user_timezone: Optional[str]
    ip_address: IPvAnyAddress

    download_time: Optional[Decimal]
    time_to_first_byte: Optional[Decimal]
    total_time: Optional[Decimal]

    parsed_ua: Optional[ParsedUA] = None

    @validator("parsed_ua", always=True)
    def fill_parsed_ua(cls, v, values, **kwargs):
        if values["ua_string"]:
            return ParsedUA.from_ua_string(values["ua_string"])
        return None

    @classmethod
    def depends(
        cls: EventCreate,
        request: Request,
        et: str,
        url: str,
        pt: str,
        psb: Optional[int] = None,
        ft: Optional[int] = None,
        ref: Optional[str] = None,
        ut: Optional[str] = None,
        ttfb: Optional[Decimal] = None,
        tt: Optional[Decimal] = None,
        dt: Optional[Decimal] = None,
    ) -> EventCreate:
        try:
            event_type = EventType(et)
        except ValueError:
            raise HTTPException(status_code=400, detail="Bad event type")
        if event_type != EventType.page_view:
            raise HTTPException(status_code=400, detail="Bad event type")

        ip_address = request.client.host
        ua_string = request.headers.get("user-agent")
        furled_url = furl(url)
        path = str(furled_url.path)
        url_params = dict(
            furled_url.args
        )  # TODO: furl.args is multidict, this conversion is lossy

        try:
            return cls(
                event_type=event_type,
                page_title=pt,
                page_size_bytes=psb,
                referrer=ref,
                user_timezone=ut,
                path=path,
                url_params=url_params,
                time_to_first_byte=ttfb,
                total_time=tt,
                download_time=dt,
                ip_address=ip_address,
                ua_string=ua_string,
                url=url,
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
