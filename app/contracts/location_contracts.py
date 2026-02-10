"""Location contracts."""

from typing import List
from pydantic import BaseModel, Field


class LocationSearchRequest(BaseModel):
    """Location search request schema."""

    q: str = Field(..., min_length=2, description="Search query")


class LocationData(BaseModel):
    """Location data schema."""

    pincode: str
    city: str
    state: str
    district: str
    area: str


class LocationSearchResponse(BaseModel):
    """Location search response schema."""

    success: bool = True
    message: str
    data: List[LocationData]
