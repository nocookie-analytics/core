from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.EventCreated)
def new_event(
    db: Session = Depends(deps.get_db),
    # request_domain: models.Domain = Depends(deps.get_request_domain),
) -> Any:
    """
    Report a new event.
    """
    return schemas.EventCreated(success=True)
