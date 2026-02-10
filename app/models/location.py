"""Location domain model."""

import uuid
from app.models.base import db, BaseModel


class Location(BaseModel):
    __tablename__ = "locations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pincode = db.Column(db.String(10), nullable=False, index=True)
    city = db.Column(db.String(100), nullable=False, index=True)
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(255), nullable=False, index=True)

    __table_args__ = (
        db.Index("idx_locations_city", "city"),
        db.Index("idx_locations_pincode", "pincode"),
        db.Index("idx_locations_area", "area"),
    )
