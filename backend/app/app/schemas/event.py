from __future__ import annotations
from app.utils.referer_parser import Referer

from decimal import Decimal
from typing import Dict, Optional, Union
from uuid import uuid4

import pydantic
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress
from pydantic.types import UUID4
from starlette.requests import Request

from app.models.event import EventType


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
    url: str
    page_title: Optional[str]
    page_size_bytes: Optional[int]
    referrer: Optional[str]
    user_timezone: Optional[str]
    user_timezone_offset: Optional[str]
    ip_address: IPvAnyAddress
    page_view_id: UUID4

    download_time: Optional[Decimal]
    time_to_first_byte: Optional[Decimal]
    total_time: Optional[Decimal]

    metric_name: Optional[str] = None
    metric_value: Optional[Decimal] = None

    @classmethod
    def depends(
        cls: EventCreate,
        request: Request,
        et: EventType,
        url: str,
        pt: Optional[str] = None,
        pvid: Optional[UUID4] = None,
        psb: Optional[int] = None,
        tz: Optional[str] = None,
        tzo: Optional[int] = None,
        ref: Optional[str] = None,
        ttfb: Optional[Decimal] = None,
        tt: Optional[Decimal] = None,
        dt: Optional[Decimal] = None,
        mn: Optional[Decimal] = None,
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

        try:
            return cls(
                event_type=event_type,
                page_title=pt,
                page_size_bytes=psb,
                referrer=ref,
                user_timezone=tz,
                user_timezone_offset=tzo,
                time_to_first_byte=ttfb,
                total_time=tt,
                download_time=dt,
                ip_address=request.client.host,
                ua_string=request.headers.get("user-agent"),
                url=url,
                page_view_id=pvid,
                metric_name=mn,
                metric_value=mv,
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
