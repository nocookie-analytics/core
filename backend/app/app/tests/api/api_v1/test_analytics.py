from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis.extra.pytz import timezones
from hypothesis.strategies import datetimes, timedeltas
import pytest
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.domain import Domain
from app.schemas.analytics import AnalyticsType
from app.tests.utils.domain import create_random_domain
from app.tests.utils.event import create_random_page_view_event
from app.tests.utils.user import create_random_user, user_authentication_headers
from app.tests.utils.utils import random_lower_string

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
        "include": [AnalyticsType.SUMMARY.value, AnalyticsType.COUNTRIES.value],
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
        "include": "summary",
    }
    response = client.get(
        f"{settings.API_V1_STR}/a/", params=data, headers=superuser_token_headers
    )
    assert response.status_code == 404, response.json()


@pytest.mark.usefixtures("override_testclient")
def test_get_analytics_success_with_data(db: Session, client: TestClient) -> None:
    # The other test is hypothesis based with no real event data, this one includes an event
    password = random_lower_string()
    user = create_random_user(db, password=password)
    domain = create_random_domain(db, owner_id=user.id)
    headers = user_authentication_headers(
        client=client, email=user.email, password=password
    )
    domain2 = create_random_domain(db)

    create_random_page_view_event(db, domain=domain)
    create_random_page_view_event(db, domain=domain2)

    data = {
        "domain_name": domain.domain_name,
        "start": datetime.now() - timedelta(minutes=1),
        "end": datetime.now() + timedelta(minutes=1),
        "include": [AnalyticsType.SUMMARY.value, AnalyticsType.COUNTRIES.value],
    }
    response = client.get(f"{settings.API_V1_STR}/a/", params=data, headers=headers)
    assert response.status_code == 200, response.json()
    json = response.json()
    assert json["summary"]["total_visits"] == 1


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
        "include": "summary",
    }
    response = client.get(f"{settings.API_V1_STR}/a/", params=data)
    assert response.status_code == 404, response.json()

    read_write_domain.public = True
    db.add(read_write_domain)
    db.commit()
    response = client.get(f"{settings.API_V1_STR}/a/", params=data)
    assert response.status_code == 200, response.json()


@pytest.mark.usefixtures("override_testclient")
def test_get_analytics_success_with_many_pages(db: Session, client: TestClient) -> None:
    # The other test is hypothesis based with no real event data, this one includes an event
    password = random_lower_string()
    user = create_random_user(db, password=password)
    domain = create_random_domain(db, owner_id=user.id)
    headers = user_authentication_headers(
        client=client, email=user.email, password=password
    )

    for i in range(120):
        create_random_page_view_event(
            db,
            domain=domain,
            create_overrides={"url": f"https://{domain.domain_name}/{i}"},
        )

    data = {
        "domain_name": domain.domain_name,
        "start": datetime.now() - timedelta(minutes=1),
        "end": datetime.now() + timedelta(minutes=1),
        "include": [AnalyticsType.PAGES.value],
    }
    response = client.get(f"{settings.API_V1_STR}/a/", params=data, headers=headers)
    assert response.status_code == 200, response.json()
    json = response.json()
    assert json["pages"] and len(json["pages"]) == 100  # default limit is 100

    response = client.get(
        f"{settings.API_V1_STR}/a/",
        params={**data, "limit": 110},
        headers=headers,
    )
    assert response.status_code == 200, response.json()
    json = response.json()
    assert json["pages"] and len(json["pages"]) == 110
