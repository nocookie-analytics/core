from __future__ import annotations
from app.utils.geolocation import get_ip_from_request
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from fastapi import Query
from fastapi.exceptions import HTTPException
import pydantic
from pydantic import BaseModel, Field
from pydantic.types import UUID4, constr
from starlette.requests import Request

from app.models.event import EventType, MetricType


# Shared properties
class EventBase(BaseModel):
    event_type: EventType


class EventCreated(BaseModel):
    success: bool = True
    error: Optional[str] = None
    page_view_id: Optional[UUID4] = None


class EventCreate(EventBase):
    @classmethod
    def depends(
        cls,
        request: Request,
        et: EventType = Query(None, description="Event type"),
        w: Optional[int] = None,
        h: Optional[int] = None,
        pvid: Optional[UUID4] = Query(None, description="Page view ID"),
        tz: Optional[str] = Query(None, description="Timezone"),
        url: Optional[str] = Query(None, description="Current page URL"),
        ref: Optional[str] = Query(None, description="Referrer"),
    ) -> PageViewEventCreate:
        try:
            event_type = EventType(et)
        except ValueError:
            raise HTTPException(status_code=400, detail="Bad event type")
        if event_type == EventType.page_view:
            pvid = UUID4(uuid4().hex)
        elif event_type in (EventType.metric, EventType.custom):
            raise HTTPException(
                status_code=400, detail="This route is only for page view events"
            )

        try:
            return PageViewEventCreate(
                event_type=event_type,
                referrer=ref or None,
                user_timezone=tz or None,
                ua_string=request.headers.get("user-agent"),
                url=url,
                width=w,
                height=h,
                page_view_id=pvid,
                ip=get_ip_from_request(request),
            )
        except pydantic.error_wrappers.ValidationError as e:
            # TODO: Return error fields from exception
            raise HTTPException(status_code=400, detail=e.errors())


class PageViewEventCreate(EventBase):
    event_type: EventType = Field(EventType.page_view, const=True)
    page_view_id: UUID4
    ua_string: str
    width: Optional[int]
    height: Optional[int]
    url: Optional[str]
    referrer: Optional[str]
    user_timezone: Optional[str]
    ip: Optional[str]

    @classmethod
    def depends(
        cls,
        request: Request,
        url: str = Query(None, description="Current page URL"),
        w: Optional[int] = Query(None, description="Screen width (pixels)"),
        h: Optional[int] = Query(None, description="Screen height (pixels)"),
        tz: Optional[str] = Query(None, description="Timezone"),
        ref: Optional[str] = Query(None, description="Referrer"),
    ):
        page_view_id = UUID4(uuid4().hex)
        try:
            return cls(
                event_type=EventType.page_view,
                referrer=ref or None,
                user_timezone=tz or None,
                ua_string=request.headers.get("user-agent"),
                url=url,
                width=w,
                height=h,
                page_view_id=page_view_id,
                ip=get_ip_from_request(request),
            )
        except pydantic.error_wrappers.ValidationError as e:
            # TODO: Return error fields from exception
            raise HTTPException(status_code=400, detail=e.errors())


class CustomEventCreate(EventBase):
    event_type: EventType = Field(EventType.custom, const=True)
    page_view_id: UUID4
    event_name: constr(min_length=2, max_length=50)
    event_value: Decimal = Decimal(1)

    @classmethod
    def depends(
        cls,
        url: str = Query(None, description="Current page URL"),
        page_view_id: UUID4 = Query(
            None, description="Page view ID (from a page view event)"
        ),
        event_name: str = Query(None, description="Event name"),
        event_value: Optional[Decimal] = Query(
            Decimal(1), description="Event value (numeric)"
        ),
    ):
        try:
            return cls(
                page_view_id=page_view_id,
                event_name=event_name,
                event_value=event_value,
            )
        except pydantic.error_wrappers.ValidationError as e:
            raise HTTPException(status_code=400, detail=e.errors())


class MetricEventCreate(EventBase):
    event_type: EventType = Field(EventType.metric, const=True)
    page_view_id: UUID4
    metric_name: MetricType
    metric_value: Decimal

    @classmethod
    def depends(
        cls,
        url: str = Query(None, description="Current page URL"),
        page_view_id: UUID4 = Query(
            None, description="Page view ID (from a page view event)"
        ),
        metric_name: str = Query(None, description="Metric name"),
        metric_value: Optional[Decimal] = Query(
            Decimal(1), description="Metric value (numeric)"
        ),
    ):
        try:
            return cls(
                page_view_id=page_view_id,
                metric_name=metric_name,
                metric_value=metric_value,
            )
        except pydantic.error_wrappers.ValidationError as e:
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
