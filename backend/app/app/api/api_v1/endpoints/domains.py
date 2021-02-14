from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Domain])
def read_domains(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve domains.
    """
    if crud.user.is_superuser(current_user):
        domains = crud.domain.get_multi(db, skip=skip, limit=limit)
    else:
        domains = crud.domain.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return domains


@router.post("/", response_model=schemas.Domain)
def create_domain(
    *,
    db: Session = Depends(deps.get_db),
    domain_in: schemas.DomainCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new domain.
    """
    domain = crud.domain.create_with_owner(
        db=db, obj_in=domain_in, owner_id=current_user.id
    )
    return domain


@router.put("/{id}", response_model=schemas.Domain)
def update_domain(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    domain_in: schemas.DomainUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an domain.
    """
    domain = crud.domain.get(db=db, id=id)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    if not crud.user.is_superuser(current_user) and (
        domain.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    domain = crud.domain.update(db=db, db_obj=domain, obj_in=domain_in)
    return domain


@router.get("/{id}", response_model=schemas.Domain)
def read_domain(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get domain by ID.
    """
    domain = crud.domain.get(db=db, id=id)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    if not crud.user.is_superuser(current_user) and (
        domain.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return domain


@router.get("/{name}", response_model=schemas.Domain)
def read_domain_by_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str,
    current_user: models.User = Depends(deps.get_current_active_user_silent),
) -> Any:
    """
    Get domain by name.
    """
    domain = crud.domain.get_by_name_check_permission(
        db=db, name=name, current_user=current_user
    )
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return domain


@router.delete("/{id}", response_model=schemas.Domain)
def delete_domain(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an domain.
    """
    domain = crud.domain.get(db=db, id=id)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    if not crud.user.is_superuser(current_user) and (
        domain.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    domain = crud.domain.remove(db=db, id=id)
    return domain
