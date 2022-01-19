import arrow
from typing import Callable, TypeVar, List, Union
from datetime import datetime
from app.schemas.analytics import AvgMetricPerDayStat, IntervalType, PageViewsPerDayStat


T = TypeVar("T", bound=Union[PageViewsPerDayStat, AvgMetricPerDayStat])


def time_bucket_gapfill(
    data: List[T],
    start: datetime,
    end: datetime,
    interval: IntervalType,
    creator: Callable,
) -> List[T]:
    """A python implementation of the time_bucket_gapfill provided by TimescaleDB."""
    existing = {row.date: row for row in data}
    for date in arrow.Arrow.span_range(interval.value, start, end):
        if date[0] not in existing:
            existing[date] = creator(date[0].datetime)
    return sorted(existing.values(), key=lambda x: x.date)
