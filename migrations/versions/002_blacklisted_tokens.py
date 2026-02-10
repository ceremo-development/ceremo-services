"""Create blacklisted_tokens table

Revision ID: 002_blacklisted_tokens
Revises: 001_rental_partners
Create Date: 2024-01-02 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "0000000002"
down_revision = "0000000001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "blacklisted_tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(length=500), nullable=False),
        sa.Column("blacklisted_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_index(
        op.f("idx_blacklisted_tokens_expires_at"),
        "blacklisted_tokens",
        ["expires_at"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        op.f("idx_blacklisted_tokens_expires_at"), table_name="blacklisted_tokens"
    )
    op.drop_table("blacklisted_tokens")
