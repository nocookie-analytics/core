from typing import Any

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.EventCreated)
def new_event(
    *,
    db: Session = Depends(deps.get_db),
    request: Request,
    event_in: schemas.EventCreate = Depends(schemas.EventCreate.depends),
    request_domain: models.Domain = Depends(deps.get_request_domain),
) -> Any:
    """
    Report a new event.
    """
    ip_address = request.client.host
    crud.event.create_with_domain(
        db, obj_in=event_in, domain_id=request_domain.id, ip_address=ip_address
    )
    return schemas.EventCreated(success=True)
