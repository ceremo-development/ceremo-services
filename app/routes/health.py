"""Health check endpoint for monitoring."""

from typing import Any, Dict, Tuple
from flask import Blueprint, jsonify
from sqlalchemy import text
from app.models.base import db

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check() -> Tuple[Dict[str, Any], int]:
    """Health check endpoint."""
    try:
        # Check database connection
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503
