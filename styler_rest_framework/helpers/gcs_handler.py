# -*- coding: utf-8 -*-
"""This is the class of handling google cloud storage"""

from io import StringIO
import time

from google.cloud import storage
from google.api_core.exceptions import ServiceUnavailable


class GCSHandler:
    """The handler of google cloud storage (GCS)

    Args:
        bucket_name (str): target bucket name of gs
        *args: placeholder
        **kwargs: placeholder

    Attributes:
        bucket : a gs bucket instance
    """

    def __init__(self, bucket_name, *args, **kwargs):
        client = storage.Client()
        self.bucket = client.get_bucket(bucket_name)
        self._BACKOFF = kwargs.get("back_off", 3)

    def get_files_from_folder(self, folder_name, retry=3):
        """Return an iterator used to find blobs in the bucket.

        Args:
            folder_name (str): folder name or prefix path

        Returns:
            an iterator used to find blobs in the bucket
        """
        try:
            return self.bucket.list_blobs(prefix=folder_name)
        except ServiceUnavailable:
            if retry > 0:
                time.sleep(self._BACKOFF)
                return self.get_files_from_folder(folder_name, retry=retry - 1)
            else:
                raise

    def download_file_as_string_with_formatter(self, file_path, retry=3):
        """Download the contents of this blob as a bytes object.

        Args:
            file_path (str): path of file

        Returns:
            The data stored in this blob.
        """
        try:
            blob = self.bucket.blob(file_path)
            return blob.download_as_string().decode("utf-8").splitlines()
        except ServiceUnavailable:
            if retry > 0:
                time.sleep(self._BACKOFF)
                return self.download_file_as_string_with_formatter(
                    file_path, retry=retry - 1
                )
            else:
                raise

    def download_file_as_stream(self, file_path, retry=3):
        """Download the contents of this blob as a StringIO object.

        Args:
            file_path (str): path of file

        Returns:
            The data stored in this blob.
        """
        try:
            blob = self.bucket.blob(file_path)
            return StringIO(blob.download_as_bytes().decode("utf-8"))
        except ServiceUnavailable:
            if retry > 0:
                time.sleep(self._BACKOFF)
                return self.download_file_as_stream(file_path, retry=retry - 1)
            else:
                raise

    def download_file_as_string(self, file_path, retry=3):
        """Download the contents of this blob as a bytes object.

        Args:
            file_path (str): path of file

        Returns:
            The data stored in this blob.
        """
        try:
            blob = self.bucket.blob(file_path)
            return blob.download_as_string()
        except ServiceUnavailable:
            if retry > 0:
                time.sleep(self._BACKOFF)
                return self.download_file_as_string(file_path, retry=retry - 1)
            else:
                raise

    def upload_file(self, file_obj, file_name, retry=3):
        """upload a file to the bucket.

        Args:
            file_obj (file object): A file handle open for reading.
            file_name (str): file name

        Raises:
            GoogleCloudError if the upload response returns an error status.
        """
        try:
            blob = self.bucket.blob(file_name)
            return blob.upload_from_file(file_obj)
        except ServiceUnavailable:
            if retry > 0:
                time.sleep(self._BACKOFF)
                return self.upload_file(file_obj, file_name, retry=retry - 1)
            else:
                raise

    def rename_file(self, old_file_name, new_file_name, retry=3):
        """rename a file from the bucket.

        Args:
            old_file_name (str): old file name
            new_file_name (str): new file name

        Raises:
            GoogleCloudError if the upload response returns an error status.
        """
        try:
            blob = self.bucket.blob(old_file_name)
            return self.bucket.rename_blob(blob, new_file_name)
        except ServiceUnavailable:
            if retry > 0:
                time.sleep(self._BACKOFF)
                return self.rename_file(old_file_name, new_file_name, retry=retry - 1)
            else:
                raise

    def put_as_string(
        self, filename: str, file_string: bytes, content_type: str, retry=3
    ):
        """Method to upload objects."""
        try:
            blob = self.bucket.blob(filename)
            return blob.upload_from_string(file_string, content_type)
        except ServiceUnavailable:
            if retry > 0:
                time.sleep(self._BACKOFF)
                return self.put_as_string(
                    filename, file_string, content_type, retry=retry - 1
                )
            else:
                raise

    def delete_file(self, filename, retry=3):
        """Deletes a file from the bucket"""
        try:
            blob = self.bucket.blob(filename)
            return blob.delete()
        except ServiceUnavailable:
            if retry > 0:
                time.sleep(self._BACKOFF)
                return self.delete_file(filename, retry=retry - 1)
            else:
                raise

    def is_exist(self, filename, retry=3):
        """Check if a file exists in the bucket"""
        try:
            blob = self.bucket.blob(filename)
            return blob.exists()
        except ServiceUnavailable:
            if retry > 0:
                time.sleep(self._BACKOFF)
                return self.is_exist(filename, retry=retry - 1)
            else:
                raise
