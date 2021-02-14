from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.models.user import User
from app.schemas.domain import DomainCreate, DomainUpdate


class CRUDDomain(CRUDBase[Domain, DomainCreate, DomainUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: DomainCreate, owner_id: int
    ) -> Domain:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Domain]:
        return (
            db.query(self.model)
            .filter(Domain.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_name(self, db: Session, name: str) -> Domain:
        return db.query(self.model).filter(Domain.domain_name == name).scalar()

    def get_by_name_check_permission(
        self, db: Session, name: str, current_user: Optional[User]
    ) -> Optional[Domain]:
        obj = db.query(self.model).filter(Domain.domain_name == name).scalar()
        if current_user:
            if (
                not crud.user.is_superuser(current_user)
                and obj.owner_id != current_user.id
            ):
                return None
        elif obj.public is not True:
            return None
        return obj


domain = CRUDDomain(Domain)
