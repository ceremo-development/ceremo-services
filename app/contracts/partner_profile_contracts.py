"""Partner Profile contracts."""

from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UpdatePartnerProfileRequest(BaseModel):
    """Update partner profile request schema."""

    businessName: str
    ownerName: str
    email: EmailStr
    phone: str
    address: str
    city: str
    state: str
    pincode: str
    businessType: str
    yearsInBusiness: str
    description: Optional[str] = None
    categories: List[str]
    serviceAreas: List[str]
    deliveryRadius: str


class PartnerProfileData(BaseModel):
    """Partner profile data schema."""

    businessName: str
    ownerName: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    pincode: str
    businessType: str
    yearsInBusiness: str
    description: Optional[str] = None
    categories: List[str]
    serviceAreas: List[str]
    deliveryRadius: str


class PartnerProfileResponse(BaseModel):
    """Partner profile response schema."""

    success: bool = True
    message: str
    data: PartnerProfileData
