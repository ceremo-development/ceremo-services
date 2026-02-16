"""Location service."""

from typing import Optional
from app.repositories.location_repository import LocationRepository
from app.services.nominatim_service import NominatimService
from app.contracts.location_contracts import LocationSearchResponse, LocationData
from app.utils.errors import ValidationError
from app.utils.logging import setup_logger

logger = setup_logger(__name__)


class LocationService:
    """Service for location operations."""

    def __init__(
        self,
        repository: LocationRepository,
        geocoding_service: Optional[NominatimService] = None,
    ):
        self.repository = repository
        self.geocoding_service = geocoding_service

    def search_locations(self, query: str) -> LocationSearchResponse:
        """Search locations by query string (hybrid: DB first, then geocoding API)."""
        if not query or len(query) < 2:
            raise ValidationError("Search query must be at least 2 characters")

        # Step 1: Check database first
        locations = self.repository.search_locations(query)

        if locations:
            logger.info(f"Found {len(locations)} locations in database")
            location_data = [
                LocationData(
                    pincode=loc.pincode,
                    city=loc.city,
                    state=loc.state,
                    district=loc.district,
                    area=loc.area,
                )
                for loc in locations
            ]
            return LocationSearchResponse(message="Locations found", data=location_data)

        # Step 2: Not found in DB? Try geocoding API
        if self.geocoding_service:
            logger.info(f"No results in DB, querying geocoding API for: {query}")
            api_results = self.geocoding_service.search_places(query)

            if api_results:
                # Step 3: Save to database for future searches
                saved_locations = self.repository.bulk_create(api_results)
                logger.info(f"Saved {len(saved_locations)} new locations to database")

                location_data = [
                    LocationData(
                        pincode=loc["pincode"],
                        city=loc["city"],
                        state=loc["state"],
                        district=loc["district"],
                        area=loc["area"],
                    )
                    for loc in api_results
                ]
                return LocationSearchResponse(
                    message="Locations found", data=location_data
                )

        # No results from DB or geocoding API
        logger.info(f"No locations found for query: {query}")
        return LocationSearchResponse(message="No locations found", data=[])
