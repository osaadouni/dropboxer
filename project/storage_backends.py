from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage



class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'pubic-read'

class MediaStorage(S3Boto3Storage):
    bucket_name = 'my-media-bucket' 


class PublicMediaStorage(S3Boto3Storage):
    location = 'media' 
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
