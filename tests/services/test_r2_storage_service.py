"""Tests for R2 storage service."""

import pytest
from io import BytesIO
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError, BotoCoreError
from app.services.r2_storage_service import R2StorageService
from app.utils.errors import ValidationError, AppError


@pytest.fixture
def mock_boto3_client():
    """Mock boto3 client."""
    with patch("app.services.r2_storage_service.boto3") as mock_boto3:
        mock_client = Mock()
        mock_client.meta.endpoint_url = "https://test.r2.cloudflarestorage.com"
        mock_boto3.client.return_value = mock_client
        yield mock_client


def test_r2_storage_service_init_success(mock_boto3_client):
    """Test successful initialization."""
    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )
    assert service.bucket == "test-bucket"
    assert service.client == mock_boto3_client


def test_r2_storage_service_init_missing_config():
    """Test initialization with missing config."""
    with pytest.raises(ValidationError, match="R2 storage configuration is incomplete"):
        R2StorageService(
            access_key="",
            secret_key="test_secret",
            endpoint="https://test.r2.cloudflarestorage.com",
            bucket="test-bucket",
        )


def test_r2_storage_service_init_failure():
    """Test initialization failure."""
    with patch("app.services.r2_storage_service.boto3.client") as mock_client:
        mock_client.side_effect = Exception("Connection failed")
        with pytest.raises(AppError, match="Storage service initialization failed"):
            R2StorageService(
                access_key="test_key",
                secret_key="test_secret",
                endpoint="https://test.r2.cloudflarestorage.com",
                bucket="test-bucket",
            )


def test_upload_success(mock_boto3_client):
    """Test successful file upload."""
    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    file = BytesIO(b"test content")
    url = service.upload(file, "test.txt", "text/plain")

    assert url == "https://test.r2.cloudflarestorage.com/test-bucket/test.txt"
    mock_boto3_client.upload_fileobj.assert_called_once()


def test_upload_without_content_type(mock_boto3_client):
    """Test file upload without content type."""
    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    file = BytesIO(b"test content")
    url = service.upload(file, "test.txt")

    assert url == "https://test.r2.cloudflarestorage.com/test-bucket/test.txt"


def test_upload_empty_key(mock_boto3_client):
    """Test upload with empty key."""
    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    file = BytesIO(b"test content")
    with pytest.raises(ValidationError, match="File key cannot be empty"):
        service.upload(file, "")


def test_upload_whitespace_key(mock_boto3_client):
    """Test upload with whitespace key."""
    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    file = BytesIO(b"test content")
    with pytest.raises(ValidationError, match="File key cannot be empty"):
        service.upload(file, "   ")


def test_upload_client_error(mock_boto3_client):
    """Test upload with client error."""
    mock_boto3_client.upload_fileobj.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "Bucket not found"}},
        "upload_fileobj",
    )

    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    file = BytesIO(b"test content")
    with pytest.raises(AppError, match="Failed to upload file"):
        service.upload(file, "test.txt")


def test_upload_botocore_error(mock_boto3_client):
    """Test upload with botocore error."""
    mock_boto3_client.upload_fileobj.side_effect = BotoCoreError()

    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    file = BytesIO(b"test content")
    with pytest.raises(AppError, match="Storage service connection failed"):
        service.upload(file, "test.txt")


def test_upload_unexpected_error(mock_boto3_client):
    """Test upload with unexpected error."""
    mock_boto3_client.upload_fileobj.side_effect = RuntimeError("Unexpected error")

    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    file = BytesIO(b"test content")
    with pytest.raises(AppError, match="File upload failed"):
        service.upload(file, "test.txt")


def test_delete_success(mock_boto3_client):
    """Test successful file deletion."""
    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    service.delete("test.txt")
    mock_boto3_client.delete_object.assert_called_once_with(
        Bucket="test-bucket", Key="test.txt"
    )


def test_delete_empty_key(mock_boto3_client):
    """Test delete with empty key."""
    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    with pytest.raises(ValidationError, match="File key cannot be empty"):
        service.delete("")


def test_delete_client_error(mock_boto3_client):
    """Test delete with client error."""
    mock_boto3_client.delete_object.side_effect = ClientError(
        {"Error": {"Code": "NoSuchKey", "Message": "Key not found"}}, "delete_object"
    )

    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    with pytest.raises(AppError, match="Failed to delete file"):
        service.delete("test.txt")


def test_delete_botocore_error(mock_boto3_client):
    """Test delete with botocore error."""
    mock_boto3_client.delete_object.side_effect = BotoCoreError()

    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    with pytest.raises(AppError, match="Storage service connection failed"):
        service.delete("test.txt")


def test_delete_unexpected_error(mock_boto3_client):
    """Test delete with unexpected error."""
    mock_boto3_client.delete_object.side_effect = RuntimeError("Unexpected error")

    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    with pytest.raises(AppError, match="File deletion failed"):
        service.delete("test.txt")


def test_get_url_success(mock_boto3_client):
    """Test get URL."""
    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    url = service.get_url("test.txt")
    assert url == "https://test.r2.cloudflarestorage.com/test-bucket/test.txt"


def test_get_url_empty_key(mock_boto3_client):
    """Test get URL with empty key."""
    service = R2StorageService(
        access_key="test_key",
        secret_key="test_secret",
        endpoint="https://test.r2.cloudflarestorage.com",
        bucket="test-bucket",
    )

    with pytest.raises(ValidationError, match="File key cannot be empty"):
        service.get_url("")
