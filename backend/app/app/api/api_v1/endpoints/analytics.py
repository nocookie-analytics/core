from __future__ import annotations
from app.models.event import DeviceType, ReferrerMediumType
from datetime import datetime
from typing import List, Optional

import arrow
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models
from app import crud
from app.api import deps
from app.schemas.analytics import AnalyticsData, AnalyticsType, IntervalType

router = APIRouter()


def get_end_date(end: Optional[datetime] = None) -> arrow.Arrow:
    return arrow.get(end) if end else arrow.now()


def get_start_date(
    end: arrow.Arrow = Depends(get_end_date), start: Optional[datetime] = None
) -> arrow.Arrow:
    start_arrow = arrow.get(start) if start else end.shift(months=-1)
    if start_arrow >= end:
        raise HTTPException(
            status_code=400, detail="End date should be after start date"
        )
    return start_arrow


@router.get("/", response_model=AnalyticsData, response_model_exclude_unset=True)
def get_analytics(
    domain_name: str,
    *,
    include: List[AnalyticsType] = Query(
        ...,
        description=(
            "To include multiple fields in result use `include=` multiple times, "
            "eg: `&include=pageviews&include=countries`"
        ),
    ),
    start: arrow.Arrow = Depends(get_start_date),
    end: arrow.Arrow = Depends(get_end_date),
    page: str = None,
    country: str = None,
    browser: str = None,
    os: str = None,
    device: DeviceType = None,
    device_brand: str = None,
    referrer_name: str = None,
    event_name: str = None,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user_silent),
    include_bots: bool = False,
    interval: IntervalType = Query(
        IntervalType.DAY,
        description="Works with per day metrics. Set interval to hour to get more granular metrics for each hour of the day",
    ),
    db: Session = Depends(deps.get_db),
    referrer_medium: ReferrerMediumType = None,
):
    # TODO: This section (getting domain/verifying ownership)
    # can be written as a reusable dependency
    domain = crud.domain.get_by_name_check_permission(
        db=db, name=domain_name, current_user=current_user
    )
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")

    return crud.event.get_analytics_from_fields(
        db=db,
        fields=include,
        start=start,
        end=end,
        domain=domain,
        country=country,
        page=page,
        browser=browser,
        os=os,
        device_brand=device_brand,
        device_type=device,
        group_limit=limit,
        include_bots=include_bots,
        referrer_name=referrer_name,
        interval=interval,
        event_name=event_name,
    )
