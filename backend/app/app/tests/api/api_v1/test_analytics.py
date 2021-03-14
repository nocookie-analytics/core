from app.schemas.analytics import AnalyticsType
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis.extra.pytz import timezones
from hypothesis.strategies import datetimes, timedeltas
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.domain import Domain

aware_datetimes = datetimes(timezones=timezones(), min_value=datetime(1500, 1, 1))


@given(
    aware_datetimes,
    timedeltas(min_value=timedelta(hours=1), max_value=timedelta(days=180)),
)
@pytest.mark.usefixtures("override_testclient")
def test_get_analytics_success(
    client: TestClient,
    mock_read_only_domain: Domain,
    superuser_token_headers: dict,
    start: datetime,
    duration: timedelta,
) -> None:
    data = {
        "domain_name": mock_read_only_domain.domain_name,
        "start": start,
        "end": start + duration,
        "include": [AnalyticsType.PAGEVIEWS.value, AnalyticsType.COUNTRIES.value],
    }
    response = client.get(
        f"{settings.API_V1_STR}/a/", params=data, headers=superuser_token_headers
    )
    assert response.status_code == 200, response.json()

    response = client.get(
        f"{settings.API_V1_STR}/a/",
        params={**data, "end": start - duration},
        headers=superuser_token_headers,
    )
    assert response.status_code == 400, response.json()


@given(
    aware_datetimes,
    timedeltas(min_value=timedelta(hours=1), max_value=timedelta(days=180)),
)
@pytest.mark.usefixtures("override_testclient")
def test_get_analytics_invalid_domain(
    client: TestClient,
    superuser_token_headers: dict,
    start: datetime,
    duration: timedelta,
) -> None:
    data = {
        "domain_name": "doesnotexist.com",
        "start": start,
        "end": start + duration,
        "include": "pageviews",
    }
    response = client.get(
        f"{settings.API_V1_STR}/a/", params=data, headers=superuser_token_headers
    )
    assert response.status_code == 404, response.json()


@pytest.mark.usefixtures("override_testclient")
def test_public_analytics(
    client: TestClient,
    read_write_domain: Domain,
    db: Session,
) -> None:
    data = {
        "domain_name": read_write_domain.domain_name,
        "start": datetime.now() - timedelta(days=1),
        "end": datetime.now(),
        "include": "pageviews",
    }
    response = client.get(f"{settings.API_V1_STR}/a/", params=data)
    assert response.status_code == 404, response.json()

    read_write_domain.public = True
    db.add(read_write_domain)
    db.commit()
    response = client.get(f"{settings.API_V1_STR}/a/", params=data)
    assert response.status_code == 200, response.json()
