"""Storage service factory."""

from typing import Optional
from app.config import Config
from app.services.r2_storage_service import R2StorageService


def get_storage_service(config: Config) -> Optional[R2StorageService]:
    """Create and configure R2 storage service."""
    # Return None if R2 is not configured
    if not all(
        [
            config.R2_ACCESS_KEY,
            config.R2_SECRET_KEY,
            config.R2_ENDPOINT,
            config.R2_BUCKET,
        ]
    ):
        return None

    return R2StorageService(
        access_key=config.R2_ACCESS_KEY,
        secret_key=config.R2_SECRET_KEY,
        endpoint=config.R2_ENDPOINT,
        bucket=config.R2_BUCKET,
    )
