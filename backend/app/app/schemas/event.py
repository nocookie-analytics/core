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
    page_view_id: UUID4

    download_time: Optional[Decimal]
    time_to_first_byte: Optional[Decimal]
    total_time: Optional[Decimal]

    metric_name: Optional[MetricType] = None
    metric_value: Optional[Decimal] = None

    ip_city_id: Optional[int]
    ip_country_iso_code: Optional[str]
    ip_continent_code: Optional[str]

    @classmethod
    def depends(
        cls: EventCreate,
        request: Request,
        et: EventType = Query(None, description="Event type"),
        url: HttpUrl = Query(None, description="URL"),
        pt: Optional[str] = Query(None, description="Page title"),
        pvid: Optional[UUID4] = Query(None, description="Page view ID"),
        psb: Optional[int] = Query(None, description="Page size bytes"),
        tz: Optional[str] = Query(None, description="Timezone"),
        tzo: Optional[int] = Query(None, description="Timezone offset"),
        ref: Optional[str] = Query(None, description="Referrer"),
        ttfb: Optional[Decimal] = Query(None, description="Time to first-byte"),
        tt: Optional[Decimal] = Query(None, description="Total time"),
        dt: Optional[Decimal] = Query(None, description="Download time"),
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
                page_title=pt or None,
                page_size_bytes=psb,
                referrer=ref or None,
                user_timezone=tz or None,
                user_timezone_offset=tzo,
                time_to_first_byte=ttfb,
                total_time=tt,
                download_time=dt,
                ua_string=request.headers.get("user-agent"),
                url=url,
                page_view_id=pvid,
                metric_name=mn,
                metric_value=mv,
                **cls._get_geolocation_info(get_ip_from_request(request)),
            )
        except pydantic.error_wrappers.ValidationError as e:
            # TODO: Return error fields from exception
            raise HTTPException(status_code=400, detail=e.errors())

    @staticmethod
    def _get_geolocation_info(
        ip_address: str,
    ) -> Dict[str, Optional[Union[int, str]]]:
        data: Dict[str, Optional[Union[str, int]]] = {}
        if ip_address:
            geolocation = get_ip_gelocation(ip_address)
            if not geolocation:
                return data
            city_id = geolocation.city.geoname_id
            country_code = geolocation.country.iso_code
            continent_code = geolocation.continent.code
            if city_id:
                data["ip_city_id"] = city_id
            if country_code:
                data["ip_country_iso_code"] = country_code
            data["ip_continent_code"] = continent_code
        return data


class EventUpdate(EventBase):
    pass


# Properties shared by models stored in DB
class EventInDBBase(EventBase):
    id: int
    domain_name: str
    owner_id: int

    class Config:
        orm_mode = True
