"""Add columns for custom events

Revision ID: 812fd3fe30c1
Revises: 4b234cc4431e
Create Date: 2022-01-03 14:55:49.518702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '812fd3fe30c1'
down_revision = '4b234cc4431e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('event_name', sa.String(), nullable=True))
    op.add_column('event', sa.Column('event_value', sa.NUMERIC(), nullable=True))
    op.create_index('ix_event_name', 'event', ['domain_id', 'event_name', 'timestamp'], unique=False, postgresql_where=sa.text('event_name IS NOT NULL'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_event_name', table_name='event')
    op.drop_column('event', 'event_value')
    op.drop_column('event', 'event_name')
    # ### end Alembic commands ###
