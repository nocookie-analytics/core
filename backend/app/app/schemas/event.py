from __future__ import annotations

from decimal import Decimal
from typing import Dict, Optional, Union
from uuid import uuid4

import pydantic
from fastapi.exceptions import HTTPException
from furl import furl
from pydantic import BaseModel, validator, Json
from pydantic.networks import IPvAnyAddress
from pydantic.types import UUID4
from starlette.requests import Request

from app.models.event import EventType
from app.models.parsed_ua import ParsedUA


# Shared properties
class EventBase(BaseModel):
    pass


class EventCreated(BaseModel):
    success: bool = True
    error: Optional[str] = None
    pvid: Optional[UUID4] = None


# Properties to receive on item creation
class EventCreate(EventBase):
    class Config:
        extra = "forbid"

    event_type: EventType
    ua_string: str
    path: str
    url: str
    url_params: Dict
    page_title: Optional[str]
    page_size_bytes: Optional[int]
    referrer: Optional[str]
    user_timezone: Optional[str]
    user_timezone_offset: Optional[str]
    ip_address: IPvAnyAddress
    page_view_id: UUID4
    metric: Optional[Dict[str, int]]

    download_time: Optional[Decimal]
    time_to_first_byte: Optional[Decimal]
    total_time: Optional[Decimal]

    parsed_ua: Optional[ParsedUA] = None
    metric_name: Optional[str] = None
    metric_value: Optional[Decimal] = None

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
        metric: Optional[Json[Dict[str, int]]] = None,
        pt: Optional[str] = None,
        pvid: Optional[UUID4] = None,
        psb: Optional[int] = None,
        ft: Optional[int] = None,
        tz: Optional[str] = None,
        tzo: Optional[int] = None,
        ref: Optional[str] = None,
        ttfb: Optional[Decimal] = None,
        tt: Optional[Decimal] = None,
        dt: Optional[Decimal] = None,
        mn: Optional[Decimal] = None
        mv: Optional[Decimal] = None,
    ) -> EventCreate:
        try:
            event_type = EventType(et)
        except ValueError:
            raise HTTPException(status_code=400, detail="Bad event type")
        if event_type == EventType.page_view:
            pvid = UUID4(uuid4().hex)
        elif event_type in (EventType.metric, EventType.custom) and not pvid:
            raise HTTPException(status_code=400, detail="Bad data")

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
                user_timezone=tz,
                user_timezone_offset=tzo,
                path=path,
                url_params=url_params,
                time_to_first_byte=ttfb,
                total_time=tt,
                download_time=dt,
                ip_address=ip_address,
                ua_string=ua_string,
                url=url,
                page_view_id=pvid,
                metric_name=mn,
                metric_value=mn,
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
