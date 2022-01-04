from __future__ import annotations
from app.utils.geolocation import get_ip_from_request
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from fastapi import Query
from fastapi.exceptions import HTTPException
import pydantic
from pydantic import BaseModel
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
    width: Optional[int]
    height: Optional[int]
    url: Optional[str]
    referrer: Optional[str]
    user_timezone: Optional[str]

    metric_name: Optional[MetricType] = None
    metric_value: Optional[Decimal] = None

    event_name: Optional[str] = None
    event_value: Optional[Decimal] = None

    ip: Optional[str]

    @classmethod
    def depends(
        cls: EventCreate,
        request: Request,
        et: EventType = Query(None, description="Event type"),
        w: Optional[int] = None,
        h: Optional[int] = None,
        pvid: Optional[UUID4] = Query(None, description="Page view ID"),
        tz: Optional[str] = Query(None, description="Timezone"),
        url: Optional[str] = Query(None, description="Current page URL"),
        ref: Optional[str] = Query(None, description="Referrer"),
        metric_name: Optional[MetricType] = Query(None, description="Metric name"),
        metric_value: Optional[Decimal] = Query(
            None,
            description="Metric value",
        ),
        event_name: Optional[str] = Query(None, description="Event name"),
        event_value: Optional[Decimal] = Query(
            None, description="Event value (integer or decimal)"
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
        elif event_type != EventType.custom and (event_name or event_value):
            raise HTTPException(
                status_code=400,
                detail="Event name and value are only valid for custom events",
            )
        elif event_type == EventType.custom:
            if not event_name:
                raise HTTPException(status_code=400)
            if not event_value:
                event_value = Decimal(1)

        try:
            return cls(
                event_type=event_type,
                referrer=ref or None,
                user_timezone=tz or None,
                ua_string=request.headers.get("user-agent"),
                url=url,
                width=w,
                height=h,
                page_view_id=pvid,
                metric_name=metric_name,
                metric_value=metric_value,
                ip=get_ip_from_request(request),
                event_name=event_name,
                event_value=event_value,
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
