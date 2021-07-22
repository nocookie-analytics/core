"""add stripe customer id

Revision ID: 71d1ad04d072
Revises: e3844e1ac67a
Create Date: 2021-07-22 13:35:02.132485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71d1ad04d072'
down_revision = 'e3844e1ac67a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('stripe_customer_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'stripe_customer_id')
    # ### end Alembic commands ###
