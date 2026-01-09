"""Cloud Storage bucket handler for file operations using the GCP client.

Provides simple get and put operations for objects in a GCS bucket.
"""

import logging
from typing import Optional, BinaryIO
from io import BytesIO

from google.cloud import storage
from google.api_core.exceptions import NotFound, GoogleAPIError

from app.core.config import settings

logger = logging.getLogger(__name__)


class S3Handler:
    """Handler for bucket operations backed by Google Cloud Storage.

    The public interface is kept compatible with the previous boto3-based
    implementation so existing callers do not need to change.
    """

    def __init__(
        self,
        bucket_name: Optional[str] = None,
    ):
        """Initialize handler with bucket info.

        Authentication is handled via Google Application Default Credentials.
        """
        self.bucket_name = bucket_name or settings.gcp_s3_bucket_name

        # Create GCS client using Application Default Credentials.
        # Ensure GOOGLE_APPLICATION_CREDENTIALS or equivalent is configured.
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def get_file(self, key: str) -> Optional[bytes]:
        """Download a file from the bucket.

        Args:
            key: object key (file path in bucket)

        Returns:
            File content as bytes, or None if file not found.
        """
        try:
            blob = self.bucket.blob(key)
            if not blob.exists(client=self.client):
                logger.warning(f"File not found: {key} in bucket: {self.bucket_name}")
                return None
            content = blob.download_as_bytes()
            logger.info(f"Successfully retrieved file: {key} from bucket: {self.bucket_name}")
            return content
        except GoogleAPIError as e:
            logger.error(f"Failed to get file {key} from GCS: {e}")
            raise

    def get_file_stream(self, key: str) -> Optional[BinaryIO]:
        """Get a file from the bucket as a streaming file-like object."""
        content = self.get_file(key)
        if content is None:
            return None
        return BytesIO(content)

    def put_file(
        self,
        key: str,
        data: bytes,
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> bool:
        """Upload a file to the bucket.

        Args:
            key: object key (file path in bucket)
            data: File content as bytes
            content_type: MIME type of the file (e.g., 'image/jpeg', 'application/pdf')
            metadata: Optional metadata dict to attach to the file

        Returns:
            True if upload succeeded, False otherwise
        """
        try:
            blob = self.bucket.blob(key)
            if metadata:
                blob.metadata = metadata

            blob.upload_from_string(
                data,
                content_type=content_type,
            )
            logger.info(f"Successfully uploaded file: {key} to bucket: {self.bucket_name}")
            return True
        except GoogleAPIError as e:
            logger.error(f"Failed to put file {key} to GCS: {e}")
            raise

    def delete_file(self, key: str) -> bool:
        """Delete a file from the bucket.

        Args:
            key: object key (file path in bucket)

        Returns:
            True if deletion succeeded
        """
        try:
            blob = self.bucket.blob(key)
            blob.delete()
            logger.info(f"Successfully deleted file: {key} from bucket: {self.bucket_name}")
            return True
        except NotFound:
            logger.warning(f"File not found when trying to delete: {key} in bucket: {self.bucket_name}")
            return False
        except GoogleAPIError as e:
            logger.error(f"Failed to delete file {key} from GCS: {e}")
            raise

    def file_exists(self, key: str) -> bool:
        """Check if a file exists in the bucket."""
        try:
            blob = self.bucket.blob(key)
            return blob.exists(client=self.client)
        except GoogleAPIError as e:
            logger.error(f"Failed to check if file {key} exists in GCS: {e}")
            raise

    def generate_presigned_url(
        self, key: str, expiration: int = 3600, http_method: str = "GET"
    ) -> Optional[str]:
        """Generate a signed URL for object access.

        Args:
            key: object key (file path in bucket)
            expiration: URL expiration time in seconds (default: 1 hour)
            http_method: HTTP method ('GET' for download, 'PUT' for upload)

        Returns:
            Signed URL string, or None if generation fails.
        """
        try:
            blob = self.bucket.blob(key)
            url = blob.generate_signed_url(
                version="v4",
                expiration=expiration,
                method=http_method,
            )
            logger.info(f"Generated signed URL for {key} (expires in {expiration}s)")
            return url
        except GoogleAPIError as e:
            logger.error(f"Failed to generate signed URL for {key}: {e}")
            return None