from __future__ import annotations
from enum import Enum
from typing import List
from fastapi import HTTPException
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
