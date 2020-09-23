from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.domain import Domain
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

    def get_by_name(self, db: Session, name: str):
        return db.query(self.model).filter(Domain.domain_name == name).scalar()


domain = CRUDDomain(Domain)
