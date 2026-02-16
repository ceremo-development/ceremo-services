"""Partner Profile repository."""

from typing import Optional, List
from app.models.partner_profile import PartnerProfile
from app.models.base import db


class PartnerProfileRepository:
    """Repository for partner profile data access."""

    def get_by_partner_id(self, partner_id: str) -> Optional[PartnerProfile]:
        """Get partner profile by partner ID."""
        return db.session.query(PartnerProfile).filter_by(partner_id=partner_id).first()

    def create(
        self,
        partner_id: str,
        business_name: str,
        owner_name: str,
        email: str,
        phone: str,
        address: str,
        city: str,
        state: str,
        pincode: str,
        business_type: str,
        years_in_business: str,
        description: str,
        categories: List[str],
        service_areas: List[str],
        delivery_radius: str,
    ) -> PartnerProfile:
        """Create new partner profile."""
        profile = PartnerProfile(
            partner_id=partner_id,
            business_name=business_name,
            owner_name=owner_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            business_type=business_type,
            years_in_business=years_in_business,
            description=description,
            categories=categories,
            service_areas=service_areas,
            delivery_radius=delivery_radius,
        )
        db.session.add(profile)
        db.session.commit()
        return profile

    def update(
        self,
        partner_id: str,
        business_name: str,
        owner_name: str,
        email: str,
        phone: str,
        address: str,
        city: str,
        state: str,
        pincode: str,
        business_type: str,
        years_in_business: str,
        description: str,
        categories: List[str],
        service_areas: List[str],
        delivery_radius: str,
    ) -> PartnerProfile:
        """Update existing partner profile."""
        profile = self.get_by_partner_id(partner_id)
        if not profile:
            raise ValueError(f"Profile not found for partner_id: {partner_id}")

        profile.business_name = business_name
        profile.owner_name = owner_name
        profile.email = email
        profile.phone = phone
        profile.address = address
        profile.city = city
        profile.state = state
        profile.pincode = pincode
        profile.business_type = business_type
        profile.years_in_business = years_in_business
        profile.description = description
        profile.categories = categories
        profile.service_areas = service_areas
        profile.delivery_radius = delivery_radius
        db.session.commit()
        return profile
