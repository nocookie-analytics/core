from __future__ import annotations
from app.models.location import Country
from app.models.event import Event
import datetime
from enum import Enum
from typing import List, Optional, Set, Tuple
import arrow
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import func, cast, DATE
from sqlalchemy.orm import Query
from starlette import status


class AnalyticsType(Enum):
    PAGEVIEWS = "pageviews"
    PAGEVIEWS_PER_DAY = "pageviews_per_day"
    COUNTRY = "countries"
    BROWSERS = "browser_families"
    OS = "os_families"
    DEVICES = "device_families"
    REFERRER_MEDIUMS = "referrer_mediums"
    REFERRER_NAMES = "referrer_names"

    @staticmethod
    def from_csv_string(include) -> List[AnalyticsType]:
        seq: Set[AnalyticsType] = set()
        invalid = []
        for item in include.split(","):
            try:
                seq.add(AnalyticsType(item))
            except ValueError:
                invalid.append(item)

        if invalid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": f"Invalid fields: {', '.join(invalid)}",
                    "hint": [t.value for t in AnalyticsType],
                },
            )
        if not seq:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "No field specified, see hint",
                    "hint": [t.value for t in AnalyticsType],
                },
            )
        return list(seq)


class PydanticArrow(datetime.datetime):
    # https://github.com/tiangolo/fastapi/issues/1285
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return arrow.get(v)


class PageViewStat(BaseModel):
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query):
        return PageViewStat(total_visits=base_query.count())


class PageViewsPerDayStat(BaseModel):
    date: datetime.date
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query) -> List[PageViewsPerDayStat]:
        rows = base_query.group_by(cast(Event.timestamp, DATE)).with_entities(
            cast(Event.timestamp, DATE), func.count()
        )
        return [PageViewsPerDayStat(date=row[0], total_visits=row[1]) for row in rows]


class BrowserStat(BaseModel):
    name: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query) -> List[BrowserStat]:
        rows = (
            base_query.group_by(Event.browser_family)
            .with_entities(Event.browser_family, func.count())
            .limit(10)
        )
        return [BrowserStat(name=row[0], total_visits=row[1]) for row in rows]


class CountryStat(BaseModel):
    name: str
    country_code: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query):
        rows: List[Tuple[str, str, int]] = (
            base_query.group_by(Event.ip_country_iso_code, Country.name)
            .with_entities(Event.ip_country_iso_code, Country.name, func.count())
            .limit(10)
        )
        return [
            CountryStat(country_code=row[0], name=row[1], total_visits=row[2])
            for row in rows
        ]


class OSStat(BaseModel):
    name: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query):

        rows: List[Tuple[str, str, int]] = (
            base_query.group_by(Event.os_family)
            .with_entities(Event.os_family, func.count())
            .limit(10)
        )
        return [OSStat(name=row[0], total_visits=row[1]) for row in rows]


class DeviceStat(BaseModel):
    name: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query):

        rows = (
            base_query.group_by(Event.device_family)
            .with_entities(Event.device_family, func.count())
            .limit(10)
        )
        return [DeviceStat(name=row[0], total_visits=row[1]) for row in rows]


class ReferrerMediumStat(BaseModel):
    medium: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query):

        rows = (
            base_query.group_by(Event.referrer_medium)
            .with_entities(Event.referrer_medium, func.count())
            .limit(10)
        )
        return [
            ReferrerMediumStat(medium=row[0].value, total_visits=row[1]) for row in rows
        ]


class ReferrerNameStat(BaseModel):
    medium: str
    name: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query):
        rows = (
            base_query.group_by(Event.referrer_medium, Event.referrer_name)
            .with_entities(Event.referrer_medium, Event.referrer_name, func.count())
            .filter(Event.referrer_name.isnot(None))
            .limit(10)
        )
        return [
            ReferrerNameStat(medium=row[0].value, name=row[1], total_visits=row[2])
            for row in rows
        ]


class AnalyticsData(BaseModel):
    start: PydanticArrow
    end: PydanticArrow
    pageviews: Optional[PageViewStat]
    browser_families: Optional[List[BrowserStat]]
    countries: Optional[List[CountryStat]]
    os_families: Optional[List[OSStat]]
    device_families: Optional[List[DeviceStat]]
    referrer_mediums: Optional[List[ReferrerMediumStat]]
    referrer_names: Optional[List[ReferrerNameStat]]
    pageviews_per_day: Optional[List[PageViewsPerDayStat]]

    class Config:
        json_encoders = {arrow.Arrow: lambda obj: obj.isoformat()}
