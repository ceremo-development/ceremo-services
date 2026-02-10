"""Location routes."""

from typing import Any, Tuple
from flask import Blueprint, jsonify, g
from app.services.location_service import LocationService
from app.contracts.location_contracts import LocationSearchRequest
from app.utils.validators import validate_query_params
from app.utils.errors import handle_controller_errors
from app.utils.logging import setup_logger

logger = setup_logger(__name__)


def create_location_routes(location_service: LocationService) -> Blueprint:
    """Create location routes blueprint."""
    location_bp = Blueprint("location", __name__)

    @location_bp.route("/search", methods=["GET"])
    @validate_query_params(LocationSearchRequest)
    @handle_controller_errors
    def search_locations() -> Tuple[Any, int]:
        """Search locations by query."""
        logger.info("Received location search request")

        query = g.validated_params["q"]
        response = location_service.search_locations(query)

        logger.info(f"Location search completed: {len(response.data)} results")
        return jsonify(response.model_dump()), 200

    return location_bp
