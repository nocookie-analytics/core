from __future__ import annotations
from app.models.event import ReferrerMediumType
from datetime import datetime
from enum import Enum
from typing import List, Set, Union
import arrow
from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status


class AnalyticsType(Enum):
    PAGEVIEWS = "pageviews"
    COUNTRY = "countries"
    BROWSERS = "browser_families"
    OS = "os_families"
    DEVICES = "device_families"
    REFERRER_MEDIUMS = "referrer_mediums"
    REFERRER_NAMES = "referrer_names"

    @staticmethod
    def from_csv_string(include) -> List[AnalyticsType]:
        seq: Set[AnalyticsType] = set()
        invalid = []
        for item in include.split(","):
            try:
                seq.add(AnalyticsType(item))
            except ValueError:
                invalid.append(item)

        if invalid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": f"Invalid fields: {', '.join(invalid)}",
                    "hint": [t.value for t in AnalyticsType],
                },
            )
        if not seq:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "No field specified, see hint",
                    "hint": [t.value for t in AnalyticsType],
                },
            )
        return list(seq)


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
    pageviews: int


class BrowserStat(BaseModel):
    name: str
    total_visits: int


class BrowserData(AnalyticsBase):
    type = AnalyticsType.BROWSERS
    browser_families: List[BrowserStat]


class CountryStat(BaseModel):
    name: str
    country_code: str
    total_visits: int


class CountryData(AnalyticsBase):
    type = AnalyticsType.COUNTRY
    countries: List[CountryStat]


class OSStat(BaseModel):
    name: str
    total_visits: int


class OSData(AnalyticsBase):
    type = AnalyticsType.OS
    os_families: List[OSStat]


class DeviceStat(BaseModel):
    name: str
    total_visits: int


class DeviceData(AnalyticsBase):
    type = AnalyticsType.DEVICES
    device_families: List[DeviceStat]


class ReferrerMediumStat(BaseModel):
    medium: str
    total_visits: int


class ReferrerMediumData(AnalyticsBase):
    type = AnalyticsType.REFERRER_MEDIUMS
    referrer_mediums: List[ReferrerMediumStat]


class ReferrerNameStat(BaseModel):
    medium: str
    name: str
    total_visits: int


class ReferrerNameData(AnalyticsBase):
    type = AnalyticsType.REFERRER_NAMES
    referrer_names: List[ReferrerNameStat]


AnalyticsDataTypes = Union[
    PageViewData,
    BrowserData,
    CountryData,
    OSData,
    DeviceData,
    ReferrerMediumData,
    ReferrerNameData,
]


class AnalyticsData(BaseModel):
    start: PydanticArrow
    end: PydanticArrow
    data: List[AnalyticsDataTypes]

    class Config:
        json_encoders = {arrow.Arrow: lambda obj: obj.isoformat()}
