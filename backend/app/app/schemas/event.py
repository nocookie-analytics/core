from __future__ import annotations
from app.utils.geolocation import get_ip_from_request, get_ip_gelocation
from decimal import Decimal
from typing import Dict, Optional, Union
from uuid import uuid4

from fastapi import Query
from fastapi.exceptions import HTTPException
import pydantic
from pydantic import BaseModel
from pydantic.networks import HttpUrl, IPvAnyAddress
from pydantic.types import UUID4
from starlette.requests import Request

from app.models.event import EventType, MetricType


# Shared properties
class EventBase(BaseModel):
    pass


class EventCreated(BaseModel):
    success: bool = True
    error: Optional[str] = None
    pvid: Optional[UUID4] = None


class EventCreate(EventBase):
    class Config:
        extra = "forbid"

    event_type: EventType
    page_view_id: UUID4
    ua_string: str
    url: Optional[str]
    referrer: Optional[str]
    user_timezone: Optional[str]

    metric_name: Optional[MetricType] = None
    metric_value: Optional[Decimal] = None

    ip: Optional[str]
    ip_country_iso_code: Optional[str]
    ip_continent_code: Optional[str]

    @classmethod
    def depends(
        cls: EventCreate,
        request: Request,
        et: EventType = Query(None, description="Event type"),
        pvid: Optional[UUID4] = Query(None, description="Page view ID"),
        tz: Optional[str] = Query(None, description="Timezone"),
        url: Optional[str] = Query(None, description="Current page URL"),
        ref: Optional[str] = Query(None, description="Referrer"),
        mn: Optional[MetricType] = Query(None, description="Metric name"),
        mv: Optional[Decimal] = Query(
            None,
            description="Metric value",
        ),
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
                referrer=ref or None,
                user_timezone=tz or None,
                ua_string=request.headers.get("user-agent"),
                url=url,
                page_view_id=pvid,
                metric_name=mn,
                metric_value=mv,
                ip=get_ip_from_request(request),
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
