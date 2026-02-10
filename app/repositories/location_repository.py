"""Location repository."""

from typing import List, Dict, Any
from sqlalchemy import or_
from app.models.location import Location
from app.models.base import db


class LocationRepository:
    """Repository for location data access."""

    def search_locations(self, query: str, limit: int = 20) -> List[Location]:
        """Search locations by query string."""
        search_pattern = f"%{query}%"
        return (
            db.session.query(Location)
            .filter(
                or_(
                    Location.city.ilike(search_pattern),
                    Location.area.ilike(search_pattern),
                    Location.pincode.like(search_pattern),
                    Location.district.ilike(search_pattern),
                )
            )
            .limit(limit)
            .all()
        )

    def bulk_create(self, locations_data: List[Dict[str, Any]]) -> List[Location]:
        """Create multiple locations at once."""
        locations = []
        for data in locations_data:
            # Check if location already exists
            existing = (
                db.session.query(Location)
                .filter_by(
                    pincode=data["pincode"],
                    city=data["city"],
                    area=data["area"],
                )
                .first()
            )
            if not existing:
                location = Location(**data)
                db.session.add(location)
                locations.append(location)

        if locations:
            db.session.commit()
        return locations
