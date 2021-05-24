"""add salt and fingerprint column

Revision ID: 5ac5050aa186
Revises: 60d6fb1b4bda
Create Date: 2021-05-24 12:29:35.773577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ac5050aa186'
down_revision = '60d6fb1b4bda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('domain', sa.Column('salt', sa.String(), nullable=True))
    op.add_column('domain', sa.Column('salt_last_changed', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.create_index(op.f('ix_domain_salt_last_changed'), 'domain', ['salt_last_changed'], unique=False)
    op.add_column('event', sa.Column('visitor_fingerprint', sa.String(), nullable=True))
    op.create_index('ix_visitor_fingerprint', 'event', ['domain_id', 'visitor_fingerprint', 'timestamp'], unique=False, postgresql_where=sa.text('visitor_fingerprint IS NOT NULL'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_visitor_fingerprint', table_name='event')
    op.drop_column('event', 'visitor_fingerprint')
    op.drop_index(op.f('ix_domain_salt_last_changed'), table_name='domain')
    op.drop_column('domain', 'salt_last_changed')
    op.drop_column('domain', 'salt')
    # ### end Alembic commands ###
