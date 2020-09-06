"""add timestamps to models

Revision ID: 6ac3ac0be773
Revises: 44042835f7cc
Create Date: 2020-09-06 15:18:17.400001

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6ac3ac0be773'
down_revision = '44042835f7cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('domain', sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('domain', sa.Column('updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.alter_column('event', 'timestamp',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True))
    op.add_column('user', sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('user', sa.Column('updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'updated')
    op.drop_column('user', 'created')
    op.alter_column('event', 'timestamp',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP())
    op.drop_column('domain', 'updated')
    op.drop_column('domain', 'created')
    # ### end Alembic commands ###
