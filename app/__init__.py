from typing import Dict, Any, Optional
from flask import Flask
from app.config import Config, get_settings


def create_app(config: Optional[Config] = None) -> Flask:
    app = Flask(__name__)

    if config is None:
        config = get_settings()

    @app.route("/")
    def index() -> Dict[str, Any]:
        return {"message": "Welcome to Ceremo Services", "status": "running"}

    @app.route("/health")
    def health_check() -> Dict[str, Any]:
        return {
            "status": "healthy",
            "environment": config.ENVIRONMENT,
            "database": "ceremo_db",
        }

    return app
