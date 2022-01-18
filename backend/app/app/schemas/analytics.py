from __future__ import annotations
import datetime
from enum import Enum
from typing import List, Optional, Union

import arrow
from pydantic import BaseModel
from sqlalchemy import Date, DateTime, cast, column, func
from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import desc
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column

from app.core.config import settings
from app.models.domain import Domain
from app.models.event import Event, MetricType


class AnalyticsType(Enum):
    PAGES = "pages"
    LIVE_VISITORS = "live_visitors"
    SUMMARY = "summary"
    SUMMARY_PREVIOUS_INTERVAL = "summary_previous_interval"
    PAGEVIEWS_PER_DAY = "pageviews_per_day"
    COUNTRIES = "countries"
    BROWSERS = "browser_families"
    OS = "os_families"
    DEVICE_BRANDS = "device_brands"
    SCREEN_SIZES = "screen_sizes"
    DEVICE_TYPES = "device_types"
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
    CUSTOM_EVENTS = "custom_events"


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


class CustomEventStat(BaseModel):
    event_name: str
    total: int

    @staticmethod
    def from_base_query(
        base_query: Query,
    ) -> List[CustomEventStat]:
        # TODO: This might be better written as a self inner join
        query = (
            base_query.with_entities(Event.event_name, func.sum(Event.event_value))
            .group_by(Event.event_name)
            .order_by(func.sum(Event.event_value))
        )
        print(query)
        return [CustomEventStat(event_name=row[0], total=row[1]) for row in query]


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
        from app.utils.db import time_bucket_gapfill

        if settings.USE_TIMESCALEDB:
            interval_text = "1 day" if interval == IntervalType.DAY else "1 hour"
            date_column = func.time_bucket_gapfill(
                interval_text, Event.timestamp, start.date(), end.date()
            )
        else:
            # Without timescale db, we can't use the time_bucket_gapfill function
            # so we have to do it manually in Python
            date_column = func.date_trunc(interval.value, Event.timestamp)

        rows = (
            base_query.group_by(column("interval"))
            .with_entities(
                date_column.label("interval"),
                func.coalesce(func.count(), 0),
                func.coalesce(func.count(func.distinct(Event.visitor_fingerprint)), 0),
            )
            .order_by("interval")
        )
        data = [
            PageViewsPerDayStat(
                date=row[0],
                total_visits=row[1],
                visitors=row[2],
            )
            for row in rows
        ]
        if settings.USE_TIMESCALEDB is False:
            data = time_bucket_gapfill(
                data,
                start,
                end,
                interval,
                creator=lambda date: PageViewsPerDayStat(
                    date=date, total_visits=0, visitors=0
                ),
            )
        return data


class AvgMetricPerDayStat(BaseModel):
    value: float
    date: datetime.datetime

    @staticmethod
    def from_base_query(
        base_query: Query,
        metric_name: MetricType,
        start: datetime.datetime,
        end: datetime.datetime,
    ) -> List[AvgMetricPerDayStat]:
        from app.utils.db import time_bucket_gapfill

        if settings.USE_TIMESCALEDB:
            date_column = func.time_bucket_gapfill(
                "1 day", Event.timestamp, start.date(), end.date()
            )
        else:
            # Without timescale db, we can't use the time_bucket_gapfill function
            # so we have to do it manually in Python
            date_column = func.date_trunc("day", Event.timestamp)

        rows = (
            base_query.group_by(column("one_day"))
            .with_entities(
                date_column.label("one_day"),
                func.coalesce(func.avg(Event.metric_value), 0).label("average"),
            )
            .filter(Event.metric_name == metric_name)
            .order_by("one_day")
        )
        data = [AvgMetricPerDayStat(date=row[0], value=row[1]) for row in rows]
        if settings.USE_TIMESCALEDB is False:
            data = time_bucket_gapfill(
                data,
                start,
                end,
                IntervalType.DAY,
                creator=lambda date: AvgMetricPerDayStat(date=date, value=0),
            )
        return data


class LiveVisitorStat:
    @staticmethod
    def from_base_query(base_query: Query) -> int:
        now = arrow.now()

        row = (
            base_query.filter(
                Event.timestamp.between(now.shift(minutes=-5).datetime, now.datetime)
            )
            .with_entities(
                func.coalesce(func.count(func.distinct(Event.visitor_fingerprint)), 0),
            )
            .one()
        )
        recent_visitor_count = row[0]
        return recent_visitor_count


class SummaryStat(BaseModel):
    total_visits: int
    bounce_rate: Optional[int]
    average_page_visit_time_seconds: float
    average_session_time_seconds: float
    visitors: int

    @staticmethod
    def _get_average_session_time(db: Session, base_query: Query) -> float:
        session_length = (Event.timestamp - Event.session_start).label("session_length")
        stmt = (
            base_query.distinct(Event.visitor_fingerprint)
            .distinct(Event.session_start)
            .filter(Event.session_start.isnot(None))
            .with_entities(session_length)
            .order_by(
                Event.visitor_fingerprint, Event.session_start, Event.timestamp.desc()
            )
        ).subquery()
        interval = (
            db.query(stmt)
            .filter(stmt.c.session_length > datetime.timedelta(0))
            .with_entities(func.avg(stmt.c.session_length))
            .one()[0]
        )
        return interval.total_seconds() if interval else 0

    @staticmethod
    def _get_average_page_visit_time(base_query: Query) -> float:
        avg_page_visit_time = (
            base_query.filter(Event.seconds_since_last_visit > text("interval '0'"))
            .with_entities(
                func.coalesce(
                    func.avg(Event.seconds_since_last_visit), text("interval '0'")
                )
            )
            .one()
        )
        return avg_page_visit_time[0].total_seconds()

    @staticmethod
    def _get_single_visit_visitors(base_query: Query) -> int:
        return (
            base_query.with_entities(Event.visitor_fingerprint)
            .group_by(Event.visitor_fingerprint)
            .having(func.count() == 1)
            .count()
        )

    @staticmethod
    def from_base_query(db: Session, base_query: Query):
        row = base_query.with_entities(
            func.coalesce(func.count(), 0),
            func.coalesce(func.count(func.distinct(Event.visitor_fingerprint)), 0),
        ).one()
        total_visits, total_visitors = row

        bounce_rate = None
        if total_visitors > 0:
            single_visit_visitors = SummaryStat._get_single_visit_visitors(base_query)
            multiple_visit_visitors = total_visitors - single_visit_visitors
            bounce_rate = (
                single_visit_visitors
                / (single_visit_visitors + multiple_visit_visitors)
            ) * 100
        return SummaryStat(
            total_visits=total_visits,
            visitors=total_visitors,
            bounce_rate=bounce_rate,
            average_page_visit_time_seconds=SummaryStat._get_average_page_visit_time(
                base_query
            ),
            average_session_time_seconds=SummaryStat._get_average_session_time(
                db, base_query
            ),
        )


class AnalyticsData(BaseModel):
    start: PydanticArrow
    end: PydanticArrow
    pages: Optional[List[AggregateStat]]
    live_visitors: Optional[int]
    summary: Optional[SummaryStat]
    summary_previous_interval: Optional[SummaryStat]

    lcp_per_day: Optional[List[AvgMetricPerDayStat]]
    cls_per_day: Optional[List[AvgMetricPerDayStat]]
    fp_per_day: Optional[List[AvgMetricPerDayStat]]
    fid_per_day: Optional[List[AvgMetricPerDayStat]]

    pageviews_per_day: Optional[List[PageViewsPerDayStat]]

    browser_families: Optional[List[AggregateStat]]
    countries: Optional[List[AggregateStat]]
    screen_sizes: Optional[List[AggregateStat]]
    os_families: Optional[List[AggregateStat]]
    device_brands: Optional[List[AggregateStat]]
    device_types: Optional[List[AggregateStat]]
    referrer_mediums: Optional[List[AggregateStat]]
    referrer_names: Optional[List[AggregateStat]]
    utm_sources: Optional[List[AggregateStat]]
    utm_mediums: Optional[List[AggregateStat]]
    utm_campaigns: Optional[List[AggregateStat]]
    utm_terms: Optional[List[AggregateStat]]
    utm_contents: Optional[List[AggregateStat]]
    custom_events: Optional[List[CustomEventStat]]

    class Config:
        json_encoders = {arrow.Arrow: lambda obj: obj.isoformat()}
