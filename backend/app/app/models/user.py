from datetime import datetime, timedelta

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Index
from app.core.config import settings

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import Date, DateTime, Enum as SQLAlchemyEnum

from app.core.products import Plan
from app.db.base_class import Base

ActivePlanEnum = SQLAlchemyEnum(
    Plan, native_enum=False, values_callable=lambda x: [e.value for e in x], length=50
)


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    domains = relationship("Domain", back_populates="owner")

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    delete_at = Column(
        DateTime(timezone=True), server_default=None, nullable=True
    )  # Used for soft-deletes

    stripe_customer_id = Column(String, unique=True, index=True)
    active_plan = Column(ActivePlanEnum, default=Plan.NO_PLAN)
    stripe_subscription_ref = Column(String, nullable=True)
    trial_end_date = Column(
        Date(),
        nullable=False,
        server_default=text(f"NOW() + ('{settings.TRIAL_PERIOD_DAYS} days')::interval"),
        default=lambda: datetime.now() + timedelta(days=settings.TRIAL_PERIOD_DAYS),
    )
    last_paid = Column(DateTime(timezone=True), nullable=True)

    ix_unique_deleted_user = Index(
        "ix_unique_deleted_user",
        email,
        delete_at,
        postgresql_where=delete_at.isnot(None),
        unique=True,
    )
    ix_unique_in_use_user = Index(
        "ix_unique_in_use_email",
        email,
        postgresql_where=delete_at.is_(None),
        unique=True,
    )
