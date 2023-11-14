"""del table tokens

Revision ID: a0b2d71242c9
Revises: 19a0200f4917
Create Date: 2023-11-13 23:45:39.355932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a0b2d71242c9"
down_revision: Union[str, None] = "19a0200f4917"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_tokens_access_token", table_name="tokens")
    op.drop_table("tokens")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tokens",
        sa.Column(
            "access_token", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "time_live",
            postgresql.INTERVAL(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="tokens_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="tokens_pkey"),
    )
    op.create_index(
        "ix_tokens_access_token", "tokens", ["access_token"], unique=False
    )
    # ### end Alembic commands ###
