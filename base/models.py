import os

from django.db import models
from django.contrib.postgres.fields import ArrayField

from .utils import get_parent, upload_path


MIN_SHORT_ID            = 2
MIN_SHORT_NAME          = 2
MAX_SHORT_NAME          = 4
MAX_SHORT_ID            = 8
MAX_LENGTH_SHORT_NAME   = 16
MAX_LENGTH_NAME         = 32
MAX_LENGTH_LONG_NAME    = 64
MAX_LENGTH_ID           = 64
MAX_LENGTH_SUB          = 128
MAX_LENGTH_URL          = 255
MAX_LENGTH_MSG          = 255
MAX_LENGTH_ADDRESS      = 255
MAX_LENGTH_LONG_URL     = 1024
MAX_LENGTH_DETAIL       = 2048

BASE_ATTRIBUTE_CHOICES = tuple((
    (status.lower(), status) for status in ['Integer', 'String', 'Boolean']
))


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        pk = str(self.pk)
        name = getattr(self, 'name', '')
        return pk + ':' + name if name else pk


class BaseTimeModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(BaseModel.Meta):
        abstract = True


class BaseOrderedModel(BaseTimeModel):
    order = models.PositiveSmallIntegerField(default=0,
                                             help_text='higher order is higher precedence')

    class Meta(BaseTimeModel.Meta):
        abstract = True
        ordering = ("order",)


class BaseActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class BaseValidManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(valid=True)


class BaseActiveModel(BaseTimeModel):
    active = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = BaseActiveManager()

    class Meta(BaseTimeModel.Meta):
        abstract = True


class BaseActiveOrderedModel(BaseOrderedModel):
    active = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = BaseActiveManager()

    class Meta(BaseOrderedModel.Meta):
        abstract = True


class BaseRole(BaseOrderedModel):
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    type = models.CharField(max_length=MAX_LENGTH_NAME, blank=True)

    class Meta(BaseOrderedModel.Meta):
        abstract = True


class BaseMediaItem(BaseTimeModel):
    file = models.FileField(upload_to=upload_path, max_length=MAX_LENGTH_URL,
                            null=True, blank=True)

    class Meta(BaseTimeModel.Meta):
        abstract = True

    def upload_path(self, filepath):
        parent_obj = get_parent(self) or self
        return os.path.join('images', parent_obj.upload_prefix(filepath))

    def upload_prefix(self, filepath, **kwargs):
        return filepath


class BaseAttribute(BaseActiveOrderedModel):
    data_type = models.CharField(max_length=MAX_LENGTH_LONG_NAME, choices=BASE_ATTRIBUTE_CHOICES)
    name = models.CharField(max_length=MAX_LENGTH_LONG_NAME)
    options = ArrayField(models.CharField(max_length=MAX_LENGTH_MSG),
                         blank=True, null=True, help_text=', separete values like IST,UTC')

    class Meta(BaseActiveOrderedModel.Meta):
        abstract = True
        unique_together = ('name',)


class BaseAttributeValue(BaseActiveOrderedModel):
    value = models.CharField(max_length=MAX_LENGTH_LONG_NAME, null=True, blank=True)

    class Meta(BaseActiveOrderedModel.Meta):
        abstract = True


class BaseLog(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=MAX_LENGTH_LONG_NAME)
    message = models.CharField(max_length=MAX_LENGTH_MSG)

    class Meta(BaseModel.Meta):
        abstract = True