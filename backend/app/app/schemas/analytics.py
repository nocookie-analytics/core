from __future__ import annotations
from app.models.location import Country
from app.models.event import Event
import datetime
from enum import Enum
from typing import List, Optional, Set, Tuple, Union
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
    UTM_SOURCES = "utm_sources"
    UTM_MEDIUMS = "utm_mediums"
    UTM_CAMPAIGNS = "utm_campaigns"
    UTM_TERMS = "utm_terms"
    UTM_CONTENTS = "utm_contents"

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


class AggregateStat(BaseModel):
    total_visits: int
    value: Union[str, Enum]

    @staticmethod
    def from_base_query(
        base_query: Query, group_by_column, *, filter_none: bool = False
    ) -> List[AggregateStat]:
        query = base_query.group_by(group_by_column).with_entities(
            group_by_column, func.count()
        )
        if filter_none is True:
            query = query.filter(group_by_column.isnot(None))
        query = query.limit(10)
        print([row for row in query])
        return [AggregateStat(value=row[0], total_visits=row[1]) for row in query]


class AggregatePerDayStat(BaseModel):
    total_visits: int
    date: datetime.date

    @staticmethod
    def from_base_query(base_query: Query) -> List[AggregatePerDayStat]:
        rows = base_query.group_by(cast(Event.timestamp, DATE)).with_entities(
            cast(Event.timestamp, DATE), func.count()
        )
        return [AggregatePerDayStat(date=row[0], total_visits=row[1]) for row in rows]


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


class UTMTermStat(BaseModel):
    term: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query) -> List[UTMTermStat]:
        rows = (
            base_query.group_by(Event.utm_term)
            .with_entities(Event.utm_term, func.count())
            .filter(Event.utm_term.isnot(None))
            .limit(10)
        )
        return [UTMTermStat(term=row[0], total_visits=row[1]) for row in rows]


class UTMSourceStat(BaseModel):
    source: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query) -> List[UTMSourceStat]:
        rows = (
            base_query.group_by(Event.utm_source)
            .with_entities(Event.utm_source, func.count())
            .filter(Event.utm_source.isnot(None))
            .limit(10)
        )
        return [UTMSourceStat(source=row[0], total_visits=row[1]) for row in rows]


class UTMMediumStat(BaseModel):
    medium: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query) -> List[UTMMediumStat]:
        rows = (
            base_query.group_by(Event.utm_medium)
            .with_entities(Event.utm_medium, func.count())
            .filter(Event.utm_medium.isnot(None))
            .limit(10)
        )
        return [UTMMediumStat(medium=row[0], total_visits=row[1]) for row in rows]


class UTMContentStat(BaseModel):
    content: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query) -> List[UTMContentStat]:
        rows = (
            base_query.group_by(Event.utm_content)
            .with_entities(Event.utm_content, func.count())
            .filter(Event.utm_content.isnot(None))
            .limit(10)
        )
        return [UTMContentStat(content=row[0], total_visits=row[1]) for row in rows]


class UTMCampaignStat(BaseModel):
    campaign: str
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query) -> List[UTMCampaignStat]:
        rows = (
            base_query.group_by(Event.utm_campaign)
            .with_entities(Event.utm_campaign, func.count())
            .filter(Event.utm_campaign.isnot(None))
            .limit(10)
        )
        return [UTMCampaignStat(campaign=row[0], total_visits=row[1]) for row in rows]


class AnalyticsData(BaseModel):
    start: PydanticArrow
    end: PydanticArrow
    pageviews: Optional[PageViewStat]
    browser_families: Optional[List[AggregateStat]]
    countries: Optional[List[AggregateStat]]
    os_families: Optional[List[AggregateStat]]
    device_families: Optional[List[AggregateStat]]
    referrer_mediums: Optional[List[AggregateStat]]
    referrer_names: Optional[List[AggregateStat]]
    pageviews_per_day: Optional[List[AggregateStat]]
    utm_sources: Optional[List[AggregateStat]]
    utm_mediums: Optional[List[AggregateStat]]
    utm_campaigns: Optional[List[AggregateStat]]
    utm_terms: Optional[List[AggregateStat]]
    utm_contents: Optional[List[AggregateStat]]

    class Config:
        json_encoders = {arrow.Arrow: lambda obj: obj.isoformat()}
