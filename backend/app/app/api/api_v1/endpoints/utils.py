import json
from typing import Any, Dict

from fastapi import APIRouter, Depends, Request
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.utils.email import send_test_email
from app.utils.geolocation import get_ip_from_request

router = APIRouter()


@router.post(
    "/test-email/", response_model=schemas.Msg, status_code=201, include_in_schema=False
)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}


@router.get(
    "/debug-request/",
    status_code=200,
    include_in_schema=False,
)
def debug_request(
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Dict:
    """
    Debug request
    """
    return dict(
        request.headers.items(),
        remote_ip=get_ip_from_request(request),
        raw=json.dumps(request.headers.items()),
    )
