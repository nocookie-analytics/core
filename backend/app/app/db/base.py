# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.domain import Domain  # noqa
from app.models.user import User  # noqa
from app.models.event import Event  # noqa
