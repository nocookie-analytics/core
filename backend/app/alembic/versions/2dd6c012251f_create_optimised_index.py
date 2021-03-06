"""Create optimised index

Revision ID: 2dd6c012251f
Revises: ecb00a22b6f5
Create Date: 2020-12-14 20:49:46.352534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dd6c012251f'
down_revision = 'ecb00a22b6f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_browser_family', 'event', ['domain_id', 'browser_family', 'timestamp'], unique=False)
    op.create_index('ix_device_brand', 'event', ['domain_id', 'device_brand', 'timestamp'], unique=False)
    op.create_index('ix_device_family', 'event', ['domain_id', 'device_family', 'timestamp'], unique=False)
    op.create_index('ix_device_metric', 'event', ['domain_id', 'metric_name', 'timestamp'], unique=False)
    op.create_index('ix_device_model', 'event', ['domain_id', 'device_model', 'timestamp'], unique=False)
    op.create_index('ix_os_family', 'event', ['domain_id', 'os_family', 'timestamp'], unique=False)
    op.drop_index('ix_event_browser_family', table_name='event')
    op.drop_index('ix_event_device_brand', table_name='event')
    op.drop_index('ix_event_device_family', table_name='event')
    op.drop_index('ix_event_device_model', table_name='event')
    op.drop_index('ix_event_metric_name', table_name='event')
    op.drop_index('ix_event_os_family', table_name='event')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_event_os_family', 'event', ['os_family'], unique=False)
    op.create_index('ix_event_metric_name', 'event', ['metric_name'], unique=False)
    op.create_index('ix_event_device_model', 'event', ['device_model'], unique=False)
    op.create_index('ix_event_device_family', 'event', ['device_family'], unique=False)
    op.create_index('ix_event_device_brand', 'event', ['device_brand'], unique=False)
    op.create_index('ix_event_browser_family', 'event', ['browser_family'], unique=False)
    op.drop_index('ix_os_family', table_name='event')
    op.drop_index('ix_device_model', table_name='event')
    op.drop_index('ix_device_metric', table_name='event')
    op.drop_index('ix_device_family', table_name='event')
    op.drop_index('ix_device_brand', table_name='event')
    op.drop_index('ix_browser_family', table_name='event')
    # ### end Alembic commands ###
