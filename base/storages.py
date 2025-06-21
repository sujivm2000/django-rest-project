from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.azure_storage import AzureStorage
from storages.backends.s3boto3 import S3Boto3Storage


class StorageUtil:
    def get_file_content(self, file_name):
        file = self.open(file_name, mode='rb')  # Open the file in binary read mode
        content = file.read()  # Read the file content
        file.close()
        return content

    def delete_file(self, file_name):
        self.delete(file_name)


class BaseStorage(StorageUtil, FileSystemStorage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'media'


class MediaStorage(BaseStorage):
    location = 'media'


class StaticStorage(BaseStorage):
    location = 'static'


class S3Storage(StorageUtil, S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    custom_domain = f'{bucket_name}.s3.amazonaws.com'


class AzureBlobStorage(StorageUtil, AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.AZURE_CONTAINER
    expiration_secs = None
