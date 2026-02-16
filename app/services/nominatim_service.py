"""Nominatim (OpenStreetMap) geocoding service - Free alternative to Google Maps."""

import requests
from typing import List, Dict, Any, Optional
from app.utils.logging import setup_logger

logger = setup_logger(__name__)


class NominatimService:
    """Free geocoding service using OpenStreetMap Nominatim."""

    def __init__(
        self, country: str = "India", country_code: str = "in", result_limit: int = 10
    ):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.headers = {"User-Agent": "CeremoServices/1.0"}
        self.country = country
        self.country_code = country_code
        self.result_limit = result_limit

    def search_places(self, query: str) -> List[Dict[str, Any]]:
        """Search places using Nominatim geocoding."""
        try:
            url = f"{self.base_url}/search"
            params: Dict[str, Any] = {
                "q": f"{query}, {self.country}",
                "format": "json",
                "addressdetails": 1,
                "limit": self.result_limit,
                "countrycodes": self.country_code,
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=5)
            response.raise_for_status()
            results = response.json()

            logger.info(f"Nominatim API returned {len(results)} results")

            locations = []
            for result in results:
                location_data = self._parse_result(result)
                if location_data:
                    locations.append(location_data)

            logger.info(f"Found {len(locations)} valid locations")
            return locations

        except requests.RequestException as e:
            logger.error(f"Nominatim API request failed: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error processing Nominatim response: {str(e)}")
            return []

    def _parse_result(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse Nominatim result into location data."""
        try:
            address = result.get("address", {})

            # Extract location components
            village = address.get("village")
            town = address.get("town")
            city = address.get("city")
            municipality = address.get("municipality")
            suburb = address.get("suburb")
            neighbourhood = address.get("neighbourhood")
            locality = address.get("locality")
            district = address.get("state_district")
            state = address.get("state")
            postcode = address.get("postcode")

            # Determine the primary place name (most specific)
            place_name = (
                village
                or town
                or city
                or municipality
                or suburb
                or neighbourhood
                or locality
            )

            # Must have state and some location identifier
            if not state or not place_name:
                return None

            # Use actual place name as area, not district
            location_data = {
                "pincode": postcode if postcode else None,
                "city": city or town or village or municipality or district,
                "state": state,
                "district": district or city or town or village,
                "area": place_name,
            }

            # Use placeholder pincode if not available
            if not location_data["pincode"]:
                location_data["pincode"] = "000000"

            return location_data

        except Exception as e:
            logger.error(f"Error parsing Nominatim result: {str(e)}")
            return None
