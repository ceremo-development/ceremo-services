"""Create partner_profiles table

Revision ID: 003_partner_profiles
Revises: 002_blacklisted_tokens
Create Date: 2024-01-03 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "0000000003"
down_revision = "0000000002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "partner_profiles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("partner_id", sa.String(length=36), nullable=False),
        sa.Column("business_name", sa.String(length=255), nullable=False),
        sa.Column("owner_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("address", sa.Text(), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("pincode", sa.String(length=10), nullable=False),
        sa.Column("business_type", sa.String(length=50), nullable=False),
        sa.Column("years_in_business", sa.String(length=20), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("categories", sa.JSON(), nullable=False),
        sa.Column("service_areas", sa.JSON(), nullable=False),
        sa.Column("delivery_radius", sa.String(length=10), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["partner_id"], ["rental_partners.id"]),
        sa.UniqueConstraint("partner_id"),
    )
    op.create_index(
        op.f("idx_partner_profiles_partner_id"), "partner_profiles", ["partner_id"]
    )


def downgrade():
    op.drop_index(
        op.f("idx_partner_profiles_partner_id"), table_name="partner_profiles"
    )
    op.drop_table("partner_profiles")
