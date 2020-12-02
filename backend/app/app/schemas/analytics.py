from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Union
import arrow
from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status


class AnalyticsType(Enum):
    PAGEVIEWS = "pageviews"
    BROWSERS = "browsers"

    @staticmethod
    def from_csv_string(include) -> List[AnalyticsType]:
        seq = []
        invalid = []
        for item in include.split(","):
            try:
                seq.append(AnalyticsType(item))
            except ValueError:
                invalid.append(item)

        if invalid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid fields: {', '.join(invalid)}",
                hint=[t.value for t in AnalyticsType],
            )
        if not seq:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No fields specified, see hint",
                valid_fields=[t.value for t in AnalyticsType],
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


class PageViewData(AnalyticsBase):
    type = AnalyticsType.PAGEVIEWS


class BrowsersData(AnalyticsBase):
    type = AnalyticsType.BROWSERS


AnalyticsDataTypes = Union[PageViewData, BrowsersData]


class AnalyticsData(BaseModel):
    start: PydanticArrow
    end: PydanticArrow
    data: List[AnalyticsDataTypes]

    class Config:
        json_encoders = {arrow.Arrow: lambda obj: obj.isoformat()}
