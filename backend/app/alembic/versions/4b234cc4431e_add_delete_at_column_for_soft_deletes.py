"""add delete_at column for soft deletes

Revision ID: 4b234cc4431e
Revises: c453da3a51b0
Create Date: 2021-08-11 09:30:48.593301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b234cc4431e'
down_revision = 'c453da3a51b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_domain_domain_name', table_name='domain')
    op.add_column('domain', sa.Column('delete_at', sa.DateTime(timezone=True), nullable=True))
    op.create_index('ix_unique_deleted_domain', 'domain', ['domain_name', 'delete_at'], unique=True, postgresql_where=sa.text('delete_at IS NOT NULL'))
    op.create_index('ix_unique_in_use_domain', 'domain', ['domain_name'], unique=True, postgresql_where=sa.text('delete_at IS NULL'))
    op.add_column('user', sa.Column('delete_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_index('ix_user_email', table_name='user')
    op.create_index('ix_unique_deleted_user', 'user', ['email', 'delete_at'], unique=True, postgresql_where=sa.text('delete_at IS NOT NULL'))
    op.create_index('ix_unique_in_use_email', 'user', ['email'], unique=True, postgresql_where=sa.text('delete_at IS NULL'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_unique_in_use_email', table_name='user')
    op.drop_index('ix_unique_deleted_user', table_name='user')
    op.create_index('ix_user_email', 'user', ['email'], unique=False)
    op.drop_column('user', 'delete_at')
    op.drop_index('ix_unique_in_use_domain', table_name='domain')
    op.drop_index('ix_unique_deleted_domain', table_name='domain')
    op.create_index('ix_domain_domain_name', 'domain', ['domain_name'], unique=False)
    # ### end Alembic commands ###