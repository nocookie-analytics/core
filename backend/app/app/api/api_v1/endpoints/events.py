from typing import Any, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get(
    "/e",
    response_model=schemas.EventCreated,
    deprecated=True,
)
def new_event(
    *,
    db: Session = Depends(deps.get_db),
    event_in: schemas.event.PageViewEventCreate = Depends(
        schemas.event.EventCreate.depends
    ),
    request_domain: models.Domain = Depends(deps.get_request_domain),
) -> Any:
    """
    Report a new page view event.

    Deprecated. Use `/e/page_view` instead
    """
    crud.event.create_with_domain(
        db,
        obj_in=event_in,
        domain=request_domain,
    )
    return schemas.EventCreated(success=True, page_view_id=event_in.page_view_id)


@router.get(
    "/e/page_view",
    response_model=schemas.EventCreated,
)
def new_page_view_event(
    *,
    db: Session = Depends(deps.get_db),
    event_in: schemas.event.PageViewEventCreate = Depends(
        schemas.event.PageViewEventCreate.depends
    ),
    request_domain: models.Domain = Depends(deps.get_request_domain),
) -> Any:
    """
    Report a new page view event
    """
    crud.event.create_with_domain(
        db,
        obj_in=event_in,
        domain=request_domain,
    )
    return schemas.EventCreated(success=True, page_view_id=event_in.page_view_id)


@router.get(
    "/e/custom",
    response_model=schemas.EventCreated,
)
def new_custom_event(
    *,
    db: Session = Depends(deps.get_db),
    event_in: schemas.event.CustomEventCreate = Depends(
        schemas.event.CustomEventCreate.depends
    ),
    request_domain: models.Domain = Depends(deps.get_request_domain),
) -> Any:
    """
    Report a new custom event
    """
    crud.event.create_with_domain(
        db,
        obj_in=event_in,
        domain=request_domain,
    )
    return schemas.EventCreated(success=True, page_view_id=event_in.page_view_id)
