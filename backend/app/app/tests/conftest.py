"""
isort:skip_file
"""
import time
import os

# We override the env before doing any other imports
os.environ["POSTGRES_DB"] = "apptest"

from typing import Dict, Generator

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


@pytest.fixture(scope="session", autouse=True)
def db(request) -> Generator:
    session = SessionLocal()
    Base.metadata.create_all(bind=engine)
    init_db(session)

    def teardown():
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
