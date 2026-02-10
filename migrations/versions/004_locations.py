"""Create locations table

Revision ID: 004_locations
Revises: 003_partner_profiles
Create Date: 2024-01-04 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "0000000004"
down_revision = "0000000003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "locations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("pincode", sa.String(length=10), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("district", sa.String(length=100), nullable=False),
        sa.Column("area", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("idx_locations_city"), "locations", ["city"])
    op.create_index(op.f("idx_locations_pincode"), "locations", ["pincode"])
    op.create_index(op.f("idx_locations_area"), "locations", ["area"])


def downgrade():
    op.drop_index(op.f("idx_locations_area"), table_name="locations")
    op.drop_index(op.f("idx_locations_pincode"), table_name="locations")
    op.drop_index(op.f("idx_locations_city"), table_name="locations")
    op.drop_table("locations")
