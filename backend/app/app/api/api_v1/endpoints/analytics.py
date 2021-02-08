from __future__ import annotations
from app import models

from datetime import datetime
from typing import List, Optional

import arrow
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.analytics import AnalyticsData, AnalyticsType

router = APIRouter()


def get_end_date(end: Optional[datetime] = None):
    return arrow.get(end) if end else arrow.now()


def get_start_date(
    end: arrow.Arrow = Depends(get_end_date), start: Optional[datetime] = None
):
    start = arrow.get(start) if start else end.shift(months=-1)
    if start >= end:
        raise HTTPException(
            status_code=400, detail="End date should be after start date"
        )
    return start


@router.get("/", response_model=AnalyticsData, response_model_exclude_unset=True)
def get_analytics(
    domain_name: str,
    *,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
    start: datetime = Depends(get_start_date),
    end: datetime = Depends(get_end_date),
    include: List[AnalyticsType] = Depends(AnalyticsType.from_csv_string),
):
    # TODO: This section (getting domain/verifying ownership)
    # can be written as a reusable dependency
    domain = crud.domain.get_by_name(db=db, name=domain_name)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    if not crud.user.is_superuser(current_user) and (
        domain.owner_id != current_user.id
    ):
        raise HTTPException(status_code=404, detail="Domain not found")

    return crud.event.get_analytics_from_fields(
        db=db, fields=include, start=start, end=end, domain=domain
    )
