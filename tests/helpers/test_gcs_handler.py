"""Tests for GCSHandler
"""
from unittest.mock import MagicMock, patch
import pytest

from google.api_core.exceptions import ServiceUnavailable

from styler_rest_framework.helpers.gcs_handler import GCSHandler


class TestGetFilesFromFolder:
    """Tests for function get_files_from_folder"""

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_normal_flow(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_bucket.list_blobs.return_value = "test return"

        test_handler = GCSHandler("test_bucket_name")
        result = test_handler.get_files_from_folder("test_folder")
        assert result == "test return"
        mock_bucket.list_blobs.assert_called_once()

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_succeed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_bucket.list_blobs.side_effect = [
            ServiceUnavailable("service unavailable"),
            "test return",
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        result = test_handler.get_files_from_folder("test_folder")
        assert result == "test return"
        assert mock_bucket.list_blobs.call_count == 2

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_failed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_bucket.list_blobs.side_effect = [
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        with pytest.raises(ServiceUnavailable) as expected:
            test_handler.get_files_from_folder("test_folder")
            assert expected.value.errors == "service unavailable"


class TestDownloadFileAsStringWithFormatter:
    """Tests for function download_file_as_string_with_formatter"""

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_normal_flow(self, mock_gcs, csv_blob_from_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.download_as_string.return_value = csv_blob_from_gcs

        test_handler = GCSHandler("test_bucket_name")
        result = test_handler.download_file_as_string_with_formatter("test_file_path")
        assert len(result) == 2
        assert result[0] == "header1,header2"
        assert result[1] == "row1-1,row1-2"
        mock_bucket.blob.assert_called_once()
        mock_blob.download_as_string.assert_called_once()

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_succeed(self, mock_gcs, csv_blob_from_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.download_as_string.side_effect = [
            ServiceUnavailable("service unavailable"),
            csv_blob_from_gcs,
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        result = test_handler.download_file_as_string_with_formatter("test_file_path")
        assert len(result) == 2
        assert result[0] == "header1,header2"
        assert result[1] == "row1-1,row1-2"
        assert mock_bucket.blob.call_count == 2
        assert mock_blob.download_as_string.call_count == 2

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_failed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.download_as_string.side_effect = [
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        with pytest.raises(ServiceUnavailable) as expected:
            test_handler.download_file_as_string_with_formatter("test_file_path")
            assert expected.value.errors == "service unavailable"


class TestDownloadFileAsStream:
    """Tests for function download_file_as_stream"""

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_normal_flow(self, mock_gcs, csv_blob_from_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.download_as_bytes.return_value = csv_blob_from_gcs

        test_handler = GCSHandler("test_bucket_name")
        result = test_handler.download_file_as_stream("test_file_path")
        assert result.getvalue() == csv_blob_from_gcs.decode("utf-8")
        mock_bucket.blob.assert_called_once()
        mock_blob.download_as_bytes.assert_called_once()

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_succeed(self, mock_gcs, csv_blob_from_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.download_as_bytes.side_effect = [
            ServiceUnavailable("service unavailable"),
            csv_blob_from_gcs,
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        result = test_handler.download_file_as_stream("test_file_path")
        assert result.getvalue() == csv_blob_from_gcs.decode("utf-8")
        assert mock_bucket.blob.call_count == 2
        assert mock_blob.download_as_bytes.call_count == 2

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_failed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.download_as_bytes.side_effect = [
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        with pytest.raises(ServiceUnavailable) as expected:
            test_handler.download_file_as_stream("test_file_path")
            assert expected.value.errors == "service unavailable"


class TestDownloadFileAsString:
    """Tests for function download_file_as_string"""

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_normal_flow(self, mock_gcs, csv_blob_from_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.download_as_string.return_value = csv_blob_from_gcs

        test_handler = GCSHandler("test_bucket_name")
        result = test_handler.download_file_as_string("test_file_path")
        assert result == csv_blob_from_gcs
        mock_bucket.blob.assert_called_once()
        mock_blob.download_as_string.assert_called_once()

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_succeed(self, mock_gcs, csv_blob_from_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.download_as_string.side_effect = [
            ServiceUnavailable("service unavailable"),
            csv_blob_from_gcs,
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        result = test_handler.download_file_as_string("test_file_path")
        assert result == csv_blob_from_gcs
        assert mock_bucket.blob.call_count == 2
        assert mock_blob.download_as_string.call_count == 2

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_failed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.download_as_string.side_effect = [
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        with pytest.raises(ServiceUnavailable) as expected:
            test_handler.download_file_as_string("test_file_path")
            assert expected.value.errors == "service unavailable"


class TestUploadFile:
    """Tests for function upload_file"""

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_normal_flow(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.upload_from_file.return_value = True

        test_handler = GCSHandler("test_bucket_name")
        result = test_handler.upload_file("test_file_obj", "test_file_path")
        assert result is True
        mock_bucket.blob.assert_called_once()
        mock_blob.upload_from_file.assert_called_once()

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_succeed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.upload_from_file.side_effect = [
            ServiceUnavailable("service unavailable"),
            True,
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        result = test_handler.upload_file("test_file_obj", "test_file_path")
        assert result is True
        assert mock_bucket.blob.call_count == 2
        assert mock_blob.upload_from_file.call_count == 2

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_failed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.upload_from_file.side_effect = [
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        with pytest.raises(ServiceUnavailable) as expected:
            test_handler.upload_file("test_file_obj", "test_file_path")
            assert expected.value.errors == "service unavailable"


class TestRenameFile:
    """Tests for function rename_file"""

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_normal_flow(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_bucket.rename_blob.return_value = True

        test_handler = GCSHandler("test_bucket_name")
        result = test_handler.rename_file("old_file_name", "new_file_name")
        assert result is True
        mock_bucket.blob.assert_called_once()
        mock_bucket.rename_blob.assert_called_once()

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_succeed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_bucket.rename_blob.side_effect = [
            ServiceUnavailable("service unavailable"),
            True,
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        result = test_handler.rename_file("old_file_name", "new_file_name")
        assert result is True
        assert mock_bucket.blob.call_count == 2
        assert mock_bucket.rename_blob.call_count == 2

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_failed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_bucket.rename_blob.side_effect = [
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        with pytest.raises(ServiceUnavailable) as expected:
            test_handler.rename_file("old_file_name", "new_file_name")
            assert expected.value.errors == "service unavailable"


class TestPutAsString:
    """Tests for function put_as_string"""

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_normal_flow(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.upload_from_string.return_value = True

        test_handler = GCSHandler("test_bucket_name")
        result = test_handler.put_as_string(
            "test_file_name", "test_file_string", "test_content_type"
        )
        assert result is True
        mock_bucket.blob.assert_called_once()
        mock_blob.upload_from_string.assert_called_once()

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_succeed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.upload_from_string.side_effect = [
            ServiceUnavailable("service unavailable"),
            True,
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        result = test_handler.put_as_string(
            "test_file_name", "test_file_string", "test_content_type"
        )
        assert result is True
        assert mock_bucket.blob.call_count == 2
        assert mock_blob.upload_from_string.call_count == 2

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_failed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.upload_from_string.side_effect = [
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        with pytest.raises(ServiceUnavailable) as expected:
            test_handler.put_as_string(
                "test_file_name", "test_file_string", "test_content_type"
            )
            assert expected.value.errors == "service unavailable"


class TestDeleteFile:
    """Tests for function delete_file"""

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_normal_flow(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.delete.return_value = True

        test_handler = GCSHandler("test_bucket_name")
        result = test_handler.delete_file("test_file_name")
        assert result is True
        mock_bucket.blob.assert_called_once()
        mock_blob.delete.assert_called_once()

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_succeed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.delete.side_effect = [ServiceUnavailable("service unavailable"), True]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        result = test_handler.delete_file("test_file_name")
        assert result is True
        assert mock_bucket.blob.call_count == 2
        assert mock_blob.delete.call_count == 2

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_failed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.delete.side_effect = [
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        with pytest.raises(ServiceUnavailable) as expected:
            test_handler.delete_file("test_file_name")
            assert expected.value.errors == "service unavailable"


class TestIsExist:
    """Tests for function is_exist"""

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_normal_flow(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.exists.return_value = True

        test_handler = GCSHandler("test_bucket_name")
        result = test_handler.is_exist("test_file_name")
        assert result is True
        mock_bucket.blob.assert_called_once()
        mock_blob.exists.assert_called_once()

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_succeed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.exists.side_effect = [ServiceUnavailable("service unavailable"), True]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        result = test_handler.is_exist("test_file_name")
        assert result is True
        assert mock_bucket.blob.call_count == 2
        assert mock_blob.exists.call_count == 2

    @patch("styler_rest_framework.helpers.gcs_handler.storage.Client", autospec=True)
    def test_retry_failed(self, mock_gcs):
        mock_client = mock_gcs.return_value
        mock_client.get_bucket = MagicMock()
        mock_bucket = mock_client.get_bucket.return_value
        mock_blob = mock_bucket.blob.return_value
        mock_blob.exists.side_effect = [
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
            ServiceUnavailable("service unavailable"),
        ]

        test_handler = GCSHandler("test_bucket_name", back_off=0.1)
        with pytest.raises(ServiceUnavailable) as expected:
            test_handler.is_exist("test_file_name")
            assert expected.value.errors == "service unavailable"
