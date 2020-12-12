"""add location models

Revision ID: b3c8f054c636
Revises: 35c94a4f3c64
Create Date: 2020-11-18 18:59:22.858730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c8f054c636'
down_revision = '35c94a4f3c64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country',
    sa.Column('id', sa.String(length=2), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('asciiname', sa.String(), nullable=True),
    sa.Column('latitude', sa.NUMERIC(), nullable=True),
    sa.Column('longitude', sa.NUMERIC(), nullable=True),
    sa.Column('country_id', sa.String(length=2), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], name='fk_event_country_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('event', sa.Column('ip_city_id', sa.Integer(), nullable=True))
    op.add_column('event', sa.Column('ip_continent_code', sa.String(length=2), nullable=True))
    op.add_column('event', sa.Column('ip_country_iso_code', sa.String(length=2), nullable=True))
    op.add_column('event', sa.Column('ip_timezone', sa.String(), nullable=True))
    op.create_foreign_key('fk_event_city_id', 'event', 'city', ['ip_city_id'], ['id'])
    op.create_foreign_key('fk_event_country_id', 'event', 'country', ['ip_country_iso_code'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_event_country_id', 'event', type_='foreignkey')
    op.drop_constraint('fk_event_city_id', 'event', type_='foreignkey')
    op.drop_column('event', 'ip_timezone')
    op.drop_column('event', 'ip_country_iso_code')
    op.drop_column('event', 'ip_continent_code')
    op.drop_column('event', 'ip_city_id')
    op.drop_table('city')
    op.drop_table('country')
    # ### end Alembic commands ###