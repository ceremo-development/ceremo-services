"""Create rental_partners table

Revision ID: 001_rental_partners
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "0000000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "rental_partners",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(
        op.f("idx_rental_partners_email"), "rental_partners", ["email"], unique=True
    )


def downgrade():
    op.drop_index(op.f("idx_rental_partners_email"), table_name="rental_partners")
    op.drop_table("rental_partners")
