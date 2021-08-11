from __future__ import annotations
from typing import TYPE_CHECKING, List

from crypt import mksalt
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, Query
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Index
from sqlalchemy.sql.sqltypes import DateTime

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Domain(Base):
    id = Column(Integer, primary_key=True, index=True)

    domain_name = Column(String)

    salt = Column(String, default=mksalt)
    salt_last_changed = Column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    events: Query = relationship("Event", lazy="dynamic")

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner: User = relationship("User", back_populates="domains")

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    delete_at = Column(
        DateTime(timezone=True), server_default=None
    )  # Used for soft-deletes

    public = Column(Boolean, nullable=False, default=False, server_default="false")

    ix_unique_deleted_domain = Index(
        "ix_unique_deleted_domain",
        domain_name,
        delete_at,
        postgresql_where=delete_at.isnot(None),
        unique=True,
    )
    ix_unique_in_use_domain = Index(
        "ix_unique_in_use_domain",
        domain_name,
        postgresql_where=delete_at.is_(None),
        unique=True,
    )
