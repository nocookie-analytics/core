from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import arrow
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.analytics import AnalyticsType

router = APIRouter()


def get_end_date(end: Optional[datetime] = None):
    return arrow.get(end) if end else arrow.now()


def get_start_date(
    end: arrow.Arrow = Depends(get_end_date), start: Optional[datetime] = None
):
    return arrow.get(start) if start else end.shift(months=-1)


@router.get("/", response_model=List[AnalyticsType])
def get_analytics(
    db: Session = Depends(deps.get_db),
    start: datetime = Depends(get_start_date),
    end: datetime = Depends(get_end_date),
    include: List[AnalyticsType] = Depends(AnalyticsType.from_csv_string),
):
    if start >= end:
        raise HTTPException(
            status_code=400, detail="End date should be after start date"
        )
    return crud.event.get_analytics_from_fields(
        db=db, fields=include, start=start, end=end
    )
