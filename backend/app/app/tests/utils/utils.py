import random
import string
from typing import Dict

from hypothesis.strategies import lists, text
from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    # Hypothesis overrides random seed, which results in subsequent calls to this function generating the same string, causing unique constraints to fail sometimes, so we override the state to use random and restore it right away
    old_state = random.getstate()
    random.seed()
    random_string = "".join(random.choices(string.ascii_lowercase, k=32))
    random.setstate(old_state)
    return random_string


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def paths():
    URL_SAFE_CHARACTERS = frozenset(
        string.ascii_letters + string.digits + "$-_.+!*'(),~"
    )

    def url_encode(s) -> str:
        return "".join(c if c in URL_SAFE_CHARACTERS else "%%%02X" % ord(c) for c in s)

    return lists(text(string.printable).map(url_encode)).map("/".join)
