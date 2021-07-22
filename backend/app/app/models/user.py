from app.core.products import Plan
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.sqltypes import Enum as SQLAlchemyEnum

from app.db.base_class import Base

if TYPE_CHECKING:
    from .domain import Domain  # noqa: F401

ActivePlanEnum = SQLAlchemyEnum(
    Plan, native_enum=False, values_callable=lambda x: [e.value for e in x]
)


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    domains = relationship("Domain", back_populates="owner")

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    stripe_customer_id = Column(String)
    active_plan = Column(ActivePlanEnum, default=Plan.NO_PLAN)
