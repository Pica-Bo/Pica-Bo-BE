from unittest.mock import MagicMock, patch

import pytest

from app.util.s3_bucket_handler import S3Handler, NotFound


@patch("app.util.s3_bucket_handler.storage.Client")
def test_init_uses_provided_bucket_name(mock_client_cls):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_client_cls.return_value = mock_client

    handler = S3Handler(bucket_name="my-bucket")

    mock_client.bucket.assert_called_once_with("my-bucket")
    assert handler.bucket is mock_bucket


@patch("app.util.s3_bucket_handler.storage.Client")
def test_get_file_success(mock_client_cls):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.exists.return_value = True
    mock_blob.download_as_bytes.return_value = b"content"
    mock_client_cls.return_value = mock_client

    handler = S3Handler(bucket_name="test-bucket")

    result = handler.get_file("path/to/file.txt")

    mock_bucket.blob.assert_called_once_with("path/to/file.txt")
    mock_blob.exists.assert_called_once_with(client=mock_client)
    mock_blob.download_as_bytes.assert_called_once()
    assert result == b"content"


@patch("app.util.s3_bucket_handler.storage.Client")
def test_get_file_not_found_returns_none(mock_client_cls):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.exists.return_value = False
    mock_client_cls.return_value = mock_client

    handler = S3Handler(bucket_name="test-bucket")

    result = handler.get_file("missing.txt")

    mock_bucket.blob.assert_called_once_with("missing.txt")
    mock_blob.exists.assert_called_once_with(client=mock_client)
    mock_blob.download_as_bytes.assert_not_called()
    assert result is None


@patch("app.util.s3_bucket_handler.storage.Client")
def test_get_file_stream_wraps_bytes_in_bytesio(mock_client_cls):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.exists.return_value = True
    mock_blob.download_as_bytes.return_value = b"stream-content"
    mock_client_cls.return_value = mock_client

    handler = S3Handler(bucket_name="test-bucket")

    stream = handler.get_file_stream("file.bin")

    assert stream is not None
    assert stream.read() == b"stream-content"


@patch("app.util.s3_bucket_handler.storage.Client")
def test_put_file_uploads_with_content_type_and_metadata(mock_client_cls):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_client_cls.return_value = mock_client

    handler = S3Handler(bucket_name="test-bucket")

    data = b"hello"
    metadata = {"foo": "bar"}

    result = handler.put_file(
        key="folder/file.txt",
        data=data,
        content_type="text/plain",
        metadata=metadata,
    )

    mock_bucket.blob.assert_called_once_with("folder/file.txt")
    assert mock_blob.metadata == metadata
    mock_blob.upload_from_string.assert_called_once_with(
        data,
        content_type="text/plain",
    )
    assert result is True


@patch("app.util.s3_bucket_handler.storage.Client")
def test_delete_file_success(mock_client_cls):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_client_cls.return_value = mock_client

    handler = S3Handler(bucket_name="test-bucket")

    result = handler.delete_file("file.txt")

    mock_bucket.blob.assert_called_once_with("file.txt")
    mock_blob.delete.assert_called_once_with()
    assert result is True


@patch("app.util.s3_bucket_handler.storage.Client")
def test_delete_file_not_found_returns_false(mock_client_cls):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.delete.side_effect = NotFound("not found")
    mock_client_cls.return_value = mock_client

    handler = S3Handler(bucket_name="test-bucket")

    result = handler.delete_file("missing.txt")

    mock_bucket.blob.assert_called_once_with("missing.txt")
    mock_blob.delete.assert_called_once_with()
    assert result is False


@patch("app.util.s3_bucket_handler.storage.Client")
def test_file_exists_true_false(mock_client_cls):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_client_cls.return_value = mock_client

    handler = S3Handler(bucket_name="test-bucket")

    # Exists
    mock_blob.exists.return_value = True
    assert handler.file_exists("exists.txt") is True

    # Does not exist
    mock_blob.exists.return_value = False
    assert handler.file_exists("missing.txt") is False


@patch("app.util.s3_bucket_handler.storage.Client")
def test_generate_presigned_url_calls_signed_url(mock_client_cls):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.generate_signed_url.return_value = "https://signed-url"
    mock_client_cls.return_value = mock_client

    handler = S3Handler(bucket_name="test-bucket")

    url = handler.generate_presigned_url(
        key="file.txt",
        expiration=600,
        http_method="GET",
    )

    mock_bucket.blob.assert_called_once_with("file.txt")
    mock_blob.generate_signed_url.assert_called_once_with(
        version="v4",
        expiration=600,
        method="GET",
    )
    assert url == "https://signed-url"
