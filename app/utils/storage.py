"""Storage service factory."""

from app.config import Config
from app.services.r2_storage_service import R2StorageService


def get_storage_service(config: Config) -> R2StorageService:
    """Create and configure R2 storage service."""
    return R2StorageService(
        access_key=config.R2_ACCESS_KEY,
        secret_key=config.R2_SECRET_KEY,
        endpoint=config.R2_ENDPOINT,
        bucket=config.R2_BUCKET,
    )
