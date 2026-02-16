"""Cloudflare R2 storage service implementation."""

import boto3
from typing import BinaryIO, Optional
from botocore.exceptions import ClientError, BotoCoreError
from app.contracts.storage_contracts import StorageService
from app.utils.errors import ValidationError, AppError
from app.utils.logging import setup_logger

logger = setup_logger(__name__)


class R2StorageService(StorageService):
    """Service for Cloudflare R2 storage operations."""

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint: str,
        bucket: str,
    ):
        if not all([access_key, secret_key, endpoint, bucket]):
            raise ValidationError("R2 storage configuration is incomplete")

        self.bucket = bucket
        try:
            self.client = boto3.client(
                "s3",
                endpoint_url=endpoint,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
            logger.info("R2 storage client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize R2 client: {str(e)}")
            raise AppError("Storage service initialization failed", 500)

    def upload(
        self, file: BinaryIO, key: str, content_type: Optional[str] = None
    ) -> str:
        """Upload file to R2 storage."""
        if not key or not key.strip():
            raise ValidationError("File key cannot be empty", "key")

        try:
            extra_args = {"ContentType": content_type} if content_type else {}
            self.client.upload_fileobj(file, self.bucket, key, ExtraArgs=extra_args)
            logger.info(f"File uploaded successfully: {key}")
            return self.get_url(key)
        except ClientError as e:
            logger.error(f"R2 upload failed for key {key}: {str(e)}")
            raise AppError(f"Failed to upload file: {str(e)}", 500)
        except BotoCoreError as e:
            logger.error(f"R2 connection error for key {key}: {str(e)}")
            raise AppError("Storage service connection failed", 500)
        except Exception as e:
            logger.error(f"Unexpected error uploading {key}: {str(e)}")
            raise AppError("File upload failed", 500)

    def delete(self, key: str) -> None:
        """Delete file from R2 storage."""
        if not key or not key.strip():
            raise ValidationError("File key cannot be empty", "key")

        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            logger.info(f"File deleted successfully: {key}")
        except ClientError as e:
            logger.error(f"R2 delete failed for key {key}: {str(e)}")
            raise AppError(f"Failed to delete file: {str(e)}", 500)
        except BotoCoreError as e:
            logger.error(f"R2 connection error for key {key}: {str(e)}")
            raise AppError("Storage service connection failed", 500)
        except Exception as e:
            logger.error(f"Unexpected error deleting {key}: {str(e)}")
            raise AppError("File deletion failed", 500)

    def get_url(self, key: str) -> str:
        """Get public URL for stored file."""
        if not key or not key.strip():
            raise ValidationError("File key cannot be empty", "key")

        return f"{self.client.meta.endpoint_url}/{self.bucket}/{key}"
