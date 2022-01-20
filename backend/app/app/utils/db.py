import arrow
from typing import Callable, TypeVar, List, Union
from datetime import datetime, timezone
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
    existing = {row.date.replace(tzinfo=timezone.utc): row for row in data}
    for date in arrow.Arrow.range(
        interval.value,
        arrow.get(start).floor(interval.value),
        arrow.get(end).ceil(interval.value),
    ):
        if date.replace(tzinfo=timezone.utc) not in existing:
            existing[date] = creator(date.datetime)
    return sorted(existing.values(), key=lambda x: x.date)
