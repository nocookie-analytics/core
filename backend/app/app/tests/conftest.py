"""
isort:skip_file
"""
import socket
import os

# We override the env before doing any other imports
os.environ["POSTGRES_DB"] = "apptest"

from typing import Dict, Generator
from starlette.datastructures import Address
from starlette.requests import Request

from app.models.location import City, Country
from app.utils.geolocation import get_ip_gelocation

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base_class import Base  # noqa
from app.db.init_db import init_db
from app.db.session import SessionLocal, engine
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers
from app.tests.utils.domain import create_random_domain


@pytest.fixture(scope="session", autouse=True)
def db(request) -> Generator:
    session = SessionLocal()
    # Start from a clean slate, but first ensure that we're always
    # working with hardcoded apptest db
    assert engine.url.database == "apptest"
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db(session)
    session.execute("SELECT create_hypertable('event', 'timestamp')")

    def teardown():
        session.rollback()
        session.commit()
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(teardown)

    yield session


@pytest.fixture(scope="function", autouse=True)
def auto_rollback(db):
    db.rollback()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )


@pytest.fixture
def override_testclient(monkeypatch):
    monkeypatch.setattr(Request, "client", Address("127.0.0.1", 5000))


@pytest.fixture(scope="session")
def mock_ip_address(db):
    ip_address = socket.gethostbyname("gaganpreet.in")
    location = get_ip_gelocation(ip_address)
    db.add(Country(id=location.country.iso_code, name=location.country.name))
    db.commit()
    return ip_address


@pytest.fixture(scope="session")
def mock_read_only_domain(db):
    domain = create_random_domain(db)
    return domain


@pytest.fixture(scope="class")
def read_write_domain(db, request):
    domain = create_random_domain(db)

    def teardown():
        for event in domain.events:
            db.delete(event)
        db.delete(domain)
        db.commit()

    request.addfinalizer(teardown)
    return domain
