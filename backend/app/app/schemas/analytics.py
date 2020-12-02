from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Union
from arrow import arrow
from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status


class AnalyticsType(Enum):
    PAGEVIEWS = "pageviews"
    BROWSERS = "browsers"

    @staticmethod
    def from_csv_string(s) -> List[AnalyticsType]:
        seq = []
        invalid = []
        for item in s.split(","):
            try:
                seq.append(AnalyticsType(item))
            except ValueError:
                invalid.append(item)

        if invalid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid fields: {', '.join(invalid)}",
            )
        return seq


class PydanticArrow(datetime):
    # https://github.com/tiangolo/fastapi/issues/1285
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return arrow.get(v)


class AnalyticsBase(BaseModel):
    type: AnalyticsType
    start: PydanticArrow
    end: PydanticArrow

    class Config:
        json_encoders = {arrow.Arrow: lambda obj: obj.isoformat()}


class PageViewData(AnalyticsBase):
    type = AnalyticsType.PAGEVIEWS


class BrowsersData(AnalyticsBase):
    type = AnalyticsType.BROWSERS


AnalyticsData = Union[PageViewData, BrowsersData]
