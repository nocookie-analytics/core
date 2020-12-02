from __future__ import annotations
import arrow
from datetime import datetime
from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import AnalyticsType, schemas
from app.api import deps

router = APIRouter()


def _parse_date_range(
    start: Optional[datetime], end: Optional[datetime]
) -> Tuple[arrow.Arrow, arrow.Arrow]:
    end_obj = arrow.get(end) if end else arrow.now()
    start_obj = arrow.get(start) if start else end_obj.shift(months=-1)
    return start_obj, end_obj


@router.get("/", response_model=List[AnalyticsType])
def get_analytics(
    db: Session = Depends(deps.get_db),
    start: datetime = None,
    end: datetime = None,
    include: List[AnalyticsType] = Depends(AnalyticsType.from_csv_string),
):
    start_arrow, end_arrow = _parse_date_range(start, end)
    if start_arrow >= end_arrow:
        raise HTTPException(
            status_code=400, detail="end date should be after start date"
        )
    for field in include:
        if field == AnalyticsType.PAGEVIEWS:
            ...
        if field == AnalyticsType.BROWSERS:
            ...
