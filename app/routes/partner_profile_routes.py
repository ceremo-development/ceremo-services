"""Partner Profile routes."""

from typing import Any, Tuple
from flask import Blueprint, jsonify, g
from app.services.partner_profile_service import PartnerProfileService
from app.contracts.partner_profile_contracts import UpdatePartnerProfileRequest
from app.utils.validators import validate_json, has_permission
from app.utils.errors import handle_controller_errors
from app.utils.logging import setup_logger

logger = setup_logger(__name__)


def create_partner_profile_routes(
    profile_service: PartnerProfileService,
) -> Blueprint:
    """Create partner profile routes blueprint."""
    profile_bp = Blueprint("partner_profile", __name__)

    @profile_bp.route("/profile", methods=["GET"])
    @has_permission()
    @handle_controller_errors
    def get_profile() -> Tuple[Any, int]:
        """Get partner profile."""
        logger.info("Received get profile request")

        response = profile_service.get_profile(g.partner_id)

        logger.info("Profile fetched successfully")
        return jsonify(response.model_dump()), 200

    @profile_bp.route("/profile", methods=["PUT"])
    @has_permission()
    @validate_json(UpdatePartnerProfileRequest)
    @handle_controller_errors
    def update_profile() -> Tuple[Any, int]:
        """Update partner profile."""
        logger.info("Received update profile request")

        data = g.validated_json
        response = profile_service.update_profile(g.partner_id, data)

        logger.info("Profile updated successfully")
        return jsonify(response.model_dump()), 200

    return profile_bp
