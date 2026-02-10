"""Partner Profile service."""

from typing import Dict, Any
from app.repositories.partner_profile_repository import PartnerProfileRepository
from app.repositories.rental_partner_repository import RentalPartnerRepository
from app.contracts.partner_profile_contracts import (
    PartnerProfileResponse,
    PartnerProfileData,
)
from app.utils.errors import NotFoundError
from app.models.rental_partner import RentalPartner


class PartnerProfileService:
    """Service for partner profile operations."""

    def __init__(
        self,
        repository: PartnerProfileRepository,
        partner_repository: RentalPartnerRepository,
    ):
        self.repository = repository
        self.partner_repository = partner_repository

    def _create_empty_profile_data(self, partner: RentalPartner) -> PartnerProfileData:
        """Create empty profile data from partner."""
        return PartnerProfileData(
            businessName="",
            ownerName=f"{partner.first_name} {partner.last_name}",
            email=partner.email,
            phone=partner.phone,
            address="",
            city="",
            state="",
            pincode="",
            businessType="",
            yearsInBusiness="",
            description="",
            categories=[],
            serviceAreas=[],
            deliveryRadius="",
        )

    def get_profile(self, partner_id: str) -> PartnerProfileResponse:
        """Get partner profile by partner ID."""
        profile = self.repository.get_by_partner_id(partner_id)

        if not profile:
            partner = self.partner_repository.find_by_id(partner_id)
            if not partner:
                raise NotFoundError("Partner", partner_id)

            return PartnerProfileResponse(
                message="Profile not found",
                data=self._create_empty_profile_data(partner),
            )

        profile_data = PartnerProfileData(
            businessName=profile.business_name,
            ownerName=profile.owner_name,
            email=profile.email,
            phone=profile.phone,
            address=profile.address,
            city=profile.city,
            state=profile.state,
            pincode=profile.pincode,
            businessType=profile.business_type,
            yearsInBusiness=profile.years_in_business,
            description=profile.description,
            categories=profile.categories,
            serviceAreas=profile.service_areas,
            deliveryRadius=profile.delivery_radius,
        )

        return PartnerProfileResponse(
            message="Profile fetched successfully", data=profile_data
        )

    def update_profile(
        self, partner_id: str, data: Dict[str, Any]
    ) -> PartnerProfileResponse:
        """Update partner profile."""
        partner = self.partner_repository.find_by_id(partner_id)
        if not partner:
            raise NotFoundError("Partner", partner_id)

        profile = self.repository.get_by_partner_id(partner_id)

        if profile:
            updated_profile = self.repository.update(
                partner_id=partner_id,
                business_name=data["businessName"],
                owner_name=data["ownerName"],
                email=data["email"],
                phone=data["phone"],
                address=data["address"],
                city=data["city"],
                state=data["state"],
                pincode=data["pincode"],
                business_type=data["businessType"],
                years_in_business=data["yearsInBusiness"],
                description=data.get("description", ""),
                categories=data["categories"],
                service_areas=data["serviceAreas"],
                delivery_radius=data["deliveryRadius"],
            )
        else:
            updated_profile = self.repository.create(
                partner_id=partner_id,
                business_name=data["businessName"],
                owner_name=data["ownerName"],
                email=data["email"],
                phone=data["phone"],
                address=data["address"],
                city=data["city"],
                state=data["state"],
                pincode=data["pincode"],
                business_type=data["businessType"],
                years_in_business=data["yearsInBusiness"],
                description=data.get("description", ""),
                categories=data["categories"],
                service_areas=data["serviceAreas"],
                delivery_radius=data["deliveryRadius"],
            )

        response_data = PartnerProfileData(
            businessName=updated_profile.business_name,
            ownerName=updated_profile.owner_name,
            email=updated_profile.email,
            phone=updated_profile.phone,
            address=updated_profile.address,
            city=updated_profile.city,
            state=updated_profile.state,
            pincode=updated_profile.pincode,
            businessType=updated_profile.business_type,
            yearsInBusiness=updated_profile.years_in_business,
            description=updated_profile.description,
            categories=updated_profile.categories,
            serviceAreas=updated_profile.service_areas,
            deliveryRadius=updated_profile.delivery_radius,
        )

        return PartnerProfileResponse(
            message="Profile updated successfully", data=response_data
        )
