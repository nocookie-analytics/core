from crypt import mksalt
from datetime import datetime, timedelta
from typing import List, Optional

from arrow.arrow import Arrow
from fastapi.encoders import jsonable_encoder
import sqlalchemy
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from app import crud
from app.crud.base import CRUDBase
from app.logger import logger
from app.models.domain import Domain
from app.models.event import Event
from app.core.config import settings
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
            .filter(Domain.delete_at.is_(None))
            .order_by(Domain.domain_name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_name(self, db: Session, name: str) -> Domain:
        return (
            db.query(self.model)
            .filter(Domain.domain_name == name, Domain.delete_at.is_(None))
            .scalar()
        )

    def get_by_name_check_permission(
        self, db: Session, name: str, current_user: Optional[User]
    ) -> Optional[Domain]:
        obj = (
            db.query(self.model)
            .filter(Domain.domain_name == name, Domain.delete_at.is_(None))
            .scalar()
        )
        if not obj:
            return None
        if obj.public is True:
            return obj
        if current_user:
            if crud.user.is_superuser(current_user) or obj.owner_id == current_user.id:
                return obj
        return None

    def mark_for_removal(self, db: Session, domain: Domain) -> None:
        domain.delete_at = datetime.now() + timedelta(
            days=settings.SOFT_DELETE_DURATION_DAYS
        )
        db.commit()

    def refresh_domain_salts(self, db: Session) -> None:
        filter_before = Arrow.now().shift(days=-1).datetime
        domains = db.query(Domain).filter(
            or_(Domain.salt_last_changed <= filter_before, Domain.salt.is_(None))
        )
        i: int = 0
        for i, domain in enumerate(domains):
            domain.salt = mksalt()
            domain.salt_last_changed = func.now()
            db.add(domain)
        db.commit()
        logger.info("Updated salt for %d domains", i)

    def delete_pending_domains(self, db: Session) -> None:
        domain_ids = (
            db.query(Domain)
            .filter(Domain.delete_at < datetime.now())
            .with_entities(Domain.id)
            .all()
        )
        domain_ids = tuple(domain_id[0] for domain_id in domain_ids)
        if domain_ids:
            db.execute(
                "delete from event where domain_id in :domain_ids",
                {"domain_ids": domain_ids},
            )
            db.execute(
                "delete from domain where id in :domain_ids", {"domain_ids": domain_ids}
            )
            db.commit()


domain = CRUDDomain(Domain)
