"""Tests for storage utility."""

import pytest
from unittest.mock import patch
from app.utils.storage import get_storage_service
from app.config import Config
from app.services.r2_storage_service import R2StorageService


@patch("app.utils.storage.R2StorageService")
def test_get_storage_service(mock_r2_service):
    """Test storage service factory."""
    config = Config(
        R2_ACCESS_KEY="test_key",
        R2_SECRET_KEY="test_secret",
        R2_ENDPOINT="https://test.r2.cloudflarestorage.com",
        R2_BUCKET="test-bucket",
    )

    get_storage_service(config)

    mock_r2_service.assert_called_once_with(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )
