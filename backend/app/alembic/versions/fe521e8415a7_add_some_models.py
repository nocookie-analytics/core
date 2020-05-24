"""Add some models

Revision ID: fe521e8415a7
Revises: d4867f3a4c0a
Create Date: 2020-05-12 20:17:02.648941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe521e8415a7'
down_revision = 'd4867f3a4c0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('domain',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain_name', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_domain_domain_name'), 'domain', ['domain_name'], unique=False)
    op.create_index(op.f('ix_domain_id'), 'domain', ['id'], unique=False)
    op.create_table('visitor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['domain_id'], ['domain.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_visitor_id'), 'visitor', ['id'], unique=False)
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=False),
    sa.Column('visitor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['visitor_id'], ['visitor.id'], ),
    sa.PrimaryKeyConstraint('id', 'timestamp')
    )
    op.create_index(op.f('ix_event_id'), 'event', ['id'], unique=False)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###

    conn = op.get_bind()
    conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
    conn.execute("SELECT create_hypertable('event', 'timestamp')")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_event_id'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_visitor_id'), table_name='visitor')
    op.drop_table('visitor')
    op.drop_index(op.f('ix_domain_id'), table_name='domain')
    op.drop_index(op.f('ix_domain_domain_name'), table_name='domain')
    op.drop_table('domain')
    # ### end Alembic commands ###