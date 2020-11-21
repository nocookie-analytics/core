from typing import List
from alembic import op
import sqlalchemy as sa


def migrate_enum(
    table_name: str,
    column_name: str,
    enum_name: str,
    old_enums: List[str],
    new_enums: List[str],
):

    enum_name_temp = f"{enum_name}_temp"
    old_type = sa.Enum(*old_enums, name=enum_name)
    new_type = sa.Enum(*new_enums, name=enum_name)
    tmp_type = sa.Enum(*new_enums, name=enum_name_temp)

    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {enum_name_temp} USING {enum_name}::text::{enum_name_temp}"
    )
    old_type.drop(op.get_bind(), checkfirst=False)
    new_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {enum_name} USING {enum_name}::text::{enum_name}"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)
