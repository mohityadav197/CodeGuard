"""convert timestamps to timezone-aware

Revision ID: c7a614c1a934
Revises: e95d8153077c
Create Date: 2026-07-12 15:07:51.438589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7a614c1a934'
down_revision: Union[str, Sequence[str], None] = 'e95d8153077c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'reviews', 'created_at',
        type_=sa.DateTime(timezone=True),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        'findings', 'created_at',
        type_=sa.DateTime(timezone=True),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        'users', 'created_at',
        type_=sa.DateTime(timezone=True),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        'users', 'last_login',
        type_=sa.DateTime(timezone=True),
        postgresql_using="last_login AT TIME ZONE 'UTC'",
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'users', 'last_login',
        type_=sa.DateTime(timezone=False),
        postgresql_using="last_login AT TIME ZONE 'UTC'",
        nullable=True,
    )
    op.alter_column(
        'users', 'created_at',
        type_=sa.DateTime(timezone=False),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        'findings', 'created_at',
        type_=sa.DateTime(timezone=False),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        'reviews', 'created_at',
        type_=sa.DateTime(timezone=False),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )
