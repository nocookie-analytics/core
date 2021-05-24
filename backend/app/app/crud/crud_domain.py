from crypt import mksalt
from typing import List, Optional
from arrow.arrow import Arrow

from fastapi.encoders import jsonable_encoder
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app import crud
from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.models.user import User
from app.schemas.domain import DomainCreate, DomainUpdate


class CRUDDomain(CRUDBase[Domain, DomainCreate, DomainUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: DomainCreate, owner_id: int
    ) -> Optional[Domain]:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
        except sqlalchemy.exc.IntegrityError:
            return None
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
        if not obj:
            return None
        if obj.public is True:
            return obj
        if current_user:
            if crud.user.is_superuser(current_user) or obj.owner_id == current_user.id:
                return obj
        return None

    def refresh_domain_salts(self, db: Session):
        filter_before = Arrow.now().shift(days=-1).datetime
        domains = db.query(Domain).filter(
            or_(Domain.salt_last_changed <= filter_before, Domain.salt.is_(None))
        )
        for domain in domains:
            domain.salt = mksalt()
            db.add(domain)
        db.commit()


domain = CRUDDomain(Domain)
