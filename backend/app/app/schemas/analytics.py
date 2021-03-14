from __future__ import annotations
import datetime
from enum import Enum
from typing import List, Optional, Set, Union

import arrow
from fastapi import HTTPException, Query as FastAPIQuery
from pydantic import BaseModel
from sqlalchemy import DATE, cast, func
from sqlalchemy.orm import Query
from starlette import status

from app.models.event import Event, MetricType


class AnalyticsType(Enum):
    PAGEVIEWS = "pageviews"
    PAGEVIEWS_PER_DAY = "pageviews_per_day"
    COUNTRIES = "countries"
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
    LCP_PER_DAY = "lcp_per_day"
    FID_PER_DAY = "fid_per_day"
    FP_PER_DAY = "fp_per_day"
    CLS_PER_DAY = "cls_per_day"


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
        return [
            AggregateStat(value=row[0] or "Unknown", total_visits=row[1])
            for row in query
        ]


class PageViewsPerDayStat(BaseModel):
    total_visits: int
    date: datetime.date

    @staticmethod
    def from_base_query(base_query: Query) -> List[PageViewsPerDayStat]:
        rows = base_query.group_by(cast(Event.timestamp, DATE)).with_entities(
            cast(Event.timestamp, DATE), func.count()
        )
        return [PageViewsPerDayStat(date=row[0], total_visits=row[1]) for row in rows]


class AvgMetricPerDayStat(BaseModel):
    value: float
    date: datetime.date

    @staticmethod
    def from_base_query(
        base_query: Query, metric_name: MetricType
    ) -> List[AvgMetricPerDayStat]:
        rows = (
            base_query.group_by(cast(Event.timestamp, DATE))
            .with_entities(cast(Event.timestamp, DATE), func.avg(Event.metric_value))
            .filter(Event.metric_name == metric_name)
        )
        return [AvgMetricPerDayStat(date=row[0], value=row[1]) for row in rows]


class PageViewStat(BaseModel):
    total_visits: int

    @staticmethod
    def from_base_query(base_query: Query):
        return PageViewStat(total_visits=base_query.count())


class AnalyticsData(BaseModel):
    start: PydanticArrow
    end: PydanticArrow
    pageviews: Optional[PageViewStat]

    lcp_per_day: Optional[List[AvgMetricPerDayStat]]
    cls_per_day: Optional[List[AvgMetricPerDayStat]]
    fp_per_day: Optional[List[AvgMetricPerDayStat]]
    fid_per_day: Optional[List[AvgMetricPerDayStat]]

    pageviews_per_day: Optional[List[PageViewsPerDayStat]]

    browser_families: Optional[List[AggregateStat]]
    countries: Optional[List[AggregateStat]]
    os_families: Optional[List[AggregateStat]]
    device_families: Optional[List[AggregateStat]]
    referrer_mediums: Optional[List[AggregateStat]]
    referrer_names: Optional[List[AggregateStat]]
    utm_sources: Optional[List[AggregateStat]]
    utm_mediums: Optional[List[AggregateStat]]
    utm_campaigns: Optional[List[AggregateStat]]
    utm_terms: Optional[List[AggregateStat]]
    utm_contents: Optional[List[AggregateStat]]

    class Config:
        json_encoders = {arrow.Arrow: lambda obj: obj.isoformat()}
