"""add stripe related fields

Revision ID: ed84c18b6b8b
Revises: e3844e1ac67a
Create Date: 2021-07-26 20:21:19.674493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed84c18b6b8b'
down_revision = 'e3844e1ac67a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active_plan', sa.Enum('no_plan', 'free', 'lite', 'medium', 'enterprise', 'cancelled', name='plan', native_enum=False), nullable=True))
    op.add_column('user', sa.Column('last_paid', sa.DateTime(timezone=True), nullable=True))
    op.add_column('user', sa.Column('stripe_customer_id', sa.String(), nullable=True))
    op.add_column('user', sa.Column('stripe_subscription_ref', sa.String(), nullable=True))
    op.add_column('user', sa.Column('trial_end_date', sa.Date(), nullable=True))
    op.create_index(op.f('ix_user_stripe_customer_id'), 'user', ['stripe_customer_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_stripe_customer_id'), table_name='user')
    op.drop_column('user', 'trial_end_date')
    op.drop_column('user', 'stripe_subscription_ref')
    op.drop_column('user', 'stripe_customer_id')
    op.drop_column('user', 'last_paid')
    op.drop_column('user', 'active_plan')
    # ### end Alembic commands ###
