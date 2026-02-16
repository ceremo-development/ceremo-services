"""Tests for storage contracts."""

import pytest
from io import BytesIO
from app.contracts.storage_contracts import StorageService


class MockStorageService(StorageService):
    """Mock implementation for testing."""

    def upload(self, file, key, content_type=None):
        return f"https://example.com/{key}"

    def delete(self, key):
        pass

    def get_url(self, key):
        return f"https://example.com/{key}"


def test_storage_service_implementation():
    """Test that StorageService can be implemented."""
    service = MockStorageService()
    file = BytesIO(b"test content")

    url = service.upload(file, "test.txt", "text/plain")
    assert url == "https://example.com/test.txt"

    service.delete("test.txt")

    url = service.get_url("test.txt")
    assert url == "https://example.com/test.txt"


def test_storage_service_abstract_methods():
    """Test abstract methods directly for coverage."""
    # Call abstract methods to achieve 100% coverage
    assert StorageService.upload.__isabstractmethod__
    assert StorageService.delete.__isabstractmethod__
    assert StorageService.get_url.__isabstractmethod__
