from fastapi.exceptions import HTTPException
import pytest
from app.schemas.analytics import AnalyticsType


@pytest.mark.parametrize("test_input", ["a,b,c", "invalid", "", "a"])
def test_from_csv_string(test_input):
    with pytest.raises(HTTPException):
        AnalyticsType.from_csv_string(test_input)


def test_from_csv_string_valid():
    assert AnalyticsType.from_csv_string("pageviews") == [AnalyticsType.PAGEVIEWS]

    assert AnalyticsType.from_csv_string("pageviews,pageviews") == [
        AnalyticsType.PAGEVIEWS
    ]

    parsed = AnalyticsType.from_csv_string("pageviews,browser_families")
    expected = [AnalyticsType.PAGEVIEWS, AnalyticsType.BROWSERS]
    assert set(parsed) == set(expected)
