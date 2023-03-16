from django.db import models

from project.storage_backends import PublicMediaStorage, PrivateMediaStorage



class DropBox(models.Model):
    title = models.CharField(max_length=30)
    document = models.FileField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Drop Boxes'


class DropBoxPrivate(models.Model):
    title = models.CharField(max_length=30)
    document = models.FileField(max_length=100, storage=PrivateMediaStorage())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Private Drop Boxes'

