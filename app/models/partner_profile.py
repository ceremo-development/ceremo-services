"""Partner Profile domain model."""

import uuid
from app.models.base import db, BaseModel, TimestampMixin


class PartnerProfile(BaseModel, TimestampMixin):
    __tablename__ = "partner_profiles"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    partner_id = db.Column(
        db.String(36), db.ForeignKey("rental_partners.id"), nullable=False, unique=True
    )
    business_name = db.Column(db.String(255), nullable=False)
    owner_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    business_type = db.Column(db.String(50), nullable=False)
    years_in_business = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    categories = db.Column(db.JSON, nullable=False)
    service_areas = db.Column(db.JSON, nullable=False)
    delivery_radius = db.Column(db.String(10), nullable=False)

    __table_args__ = (db.Index("idx_partner_profiles_partner_id", "partner_id"),)
