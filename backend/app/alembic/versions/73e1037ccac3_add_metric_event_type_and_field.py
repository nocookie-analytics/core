"""Add metric event type and field

Revision ID: 73e1037ccac3
Revises: 9a684e63e7fa
Create Date: 2020-11-21 14:18:47.028384

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic_helpers import migrate_enum
from app.models.event import EventType

# revision identifiers, used by Alembic.
revision = "73e1037ccac3"
down_revision = "9a684e63e7fa"
branch_labels = None
depends_on = None

new_enums = sorted(v.value for v in EventType)
old_enums = [v for v in new_enums if v != "metric"]


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "event",
        sa.Column("metric", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    migrate_enum("event", "event_type", "event_type", old_enums, new_enums)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("event", "metric")
    migrate_enum("event", "event_type", "event_type", new_enums, old_enums)
    # ### end Alembic commands ###
