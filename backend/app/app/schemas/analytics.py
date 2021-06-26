from __future__ import annotations
import datetime
from enum import Enum
from typing import List, Optional, Union

import arrow
from pydantic import BaseModel
from sqlalchemy import func, column
from sqlalchemy.orm import Query
from sqlalchemy.sql import desc
from sqlalchemy.sql.schema import Column

from app.models.event import Event, MetricType


class AnalyticsType(Enum):
    PAGES = "pages"
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


class IntervalType(Enum):
    DAY = "day"
    HOUR = "hour"


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
    visitors: int
    value: Union[str, Enum]

    @staticmethod
    def from_base_query(
        base_query: Query,
        group_by_column: Column,
        group_limit: int,
        *,
        filter_none: bool = False
    ) -> List[AggregateStat]:
        query = (
            base_query.group_by(group_by_column)
            .with_entities(
                group_by_column,
                func.count().label("total_visits"),
                func.count(func.distinct(Event.visitor_fingerprint)).label("visitors"),
            )
            .order_by(desc("visitors"))
        )
        if filter_none is True:
            query = query.filter(group_by_column.isnot(None))
        query = query.limit(group_limit)
        return [
            AggregateStat(
                value=row[0] or "Unknown", total_visits=row[1], visitors=row[2]
            )
            for row in query
        ]


class PageViewsPerDayStat(BaseModel):
    total_visits: int
    visitors: int
    date: datetime.datetime

    @staticmethod
    def from_base_query(
        base_query: Query,
        start: datetime.datetime,
        end: datetime.datetime,
        interval: IntervalType,
    ) -> List[PageViewsPerDayStat]:
        interval_text = "1 day"
        if interval == IntervalType.HOUR:
            interval_text = "1 hour"
        rows = (
            base_query.group_by(column("interval"))
            .with_entities(
                func.time_bucket_gapfill(
                    interval_text, Event.timestamp, start.date(), end.date()
                ).label("interval"),
                func.coalesce(func.count(), 0),
                func.coalesce(func.count(func.distinct(Event.visitor_fingerprint)), 0),
            )
            .order_by("interval")
        )
        return [
            PageViewsPerDayStat(date=row[0], total_visits=row[1], visitors=row[2])
            for row in rows
        ]


class AvgMetricPerDayStat(BaseModel):
    value: float
    date: datetime.date

    @staticmethod
    def from_base_query(
        base_query: Query,
        metric_name: MetricType,
        start: datetime.datetime,
        end: datetime.datetime,
    ) -> List[AvgMetricPerDayStat]:
        rows = (
            base_query.group_by(column("one_day"))
            .with_entities(
                func.time_bucket_gapfill("1 day", Event.timestamp, start, end).label(
                    "one_day"
                ),
                func.coalesce(func.avg(Event.metric_value), 0).label("average"),
            )
            .filter(Event.metric_name == metric_name)
            .order_by("one_day")
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
    pages: Optional[List[AggregateStat]]
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
