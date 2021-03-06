from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.models.user import User
from app.schemas.user import UserCreate, UserStripeInfoUpdate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return (
            db.query(User).filter(User.email == email, User.delete_at.is_(None)).first()
        )

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def mark_for_removal(self, db: Session, user: User) -> None:
        user.delete_at = datetime.now() + timedelta(
            days=settings.SOFT_DELETE_DURATION_DAYS
        )
        db.commit()

    def update_stripe_info(
        self, db: Session, *, user_obj: User, obj_in: UserStripeInfoUpdate
    ):
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=user_obj, obj_in=update_data)

    def delete_pending_users(self, db: Session) -> None:
        user_ids = (
            db.query(User)
            .filter(User.delete_at < datetime.now())
            .with_entities(User.id)
            .all()
        )
        user_ids = tuple(user_id[0] for user_id in user_ids)
        if user_ids:
            db.execute(
                "delete from event where domain_id in (select id from domain where owner_id in :user_ids)",
                {"user_ids": user_ids},
            )
            db.execute(
                "delete from domain where owner_id in :user_ids", {"user_ids": user_ids}
            )
            db.execute(
                'delete from "user" where id in :user_ids', {"user_ids": user_ids}
            )
            db.commit()


user = CRUDUser(User)
