"""Storage service contracts."""

from abc import ABC, abstractmethod
from typing import BinaryIO, Optional


class StorageService(ABC):
    """Abstract storage service interface."""

    @abstractmethod
    def upload(
        self, file: BinaryIO, key: str, content_type: Optional[str] = None
    ) -> str:
        """Upload file to storage."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete file from storage."""
        pass

    @abstractmethod
    def get_url(self, key: str) -> str:
        """Get public URL for stored file."""
        pass
