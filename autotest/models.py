import json
import os

from django.db import models

from base.models import MAX_LENGTH_NAME, MAX_LENGTH_ADDRESS, BaseModel, BaseTimeModel


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class JsonData(BaseModel):
    data = models.JSONField()

    def __str__(self):
        return str(self.id)


class BaseCategory(BaseTimeModel):

    APP_CHOICES = [(k, v) for k, v in (json.loads(os.environ['AUTOTEST_APP_LIST'])).items()]

    CATEGORY_CHOICES = [(k, v) for k, v in (json.loads(os.environ['AUTOTEST_CATEGORY_LIST'])).items()]

    app = models.CharField(max_length=MAX_LENGTH_NAME, null=True, blank=True, choices=APP_CHOICES)

    source = models.CharField(max_length=MAX_LENGTH_ADDRESS, null=True, blank=True)

    category = models.CharField(max_length=MAX_LENGTH_NAME, null=True, blank=True, choices=CATEGORY_CHOICES)

    class Meta(BaseTimeModel.Meta):
        abstract = True


class InputGroup(BaseModel):
    type = models.CharField(max_length=MAX_LENGTH_NAME, help_text='source, category etc.,')
    name = models.CharField(max_length=MAX_LENGTH_NAME)

    class Meta(BaseModel.Meta):
        unique_together = ('type', 'name',)

    def __str__(self):
        return f"{self.type}/{self.name}"


class Input(BaseCategory):
    name = models.CharField(max_length=MAX_LENGTH_ADDRESS, unique=True)

    parent = models.ForeignKey('Input', null=True, blank=True, on_delete=models.CASCADE, related_name='child_inputs')

    json = models.ForeignKey(JsonData, on_delete=models.CASCADE, related_name='inputs')

    active = models.BooleanField(default=False)
    version = models.PositiveSmallIntegerField(default=1)

    groups = models.ManyToManyField(InputGroup, blank=True)

    objects = models.Manager()

    active_objects = ActiveManager()

    def __str__(self):
        return f"{self.name}"


class TestCaseActiveManager(ActiveManager):
    def get_queryset(self):
        return super().get_queryset().filter(input__active=True)


class TestCase(BaseCategory):
    name = models.CharField(max_length=MAX_LENGTH_ADDRESS, unique=True)

    input = models.ForeignKey(Input, on_delete=models.CASCADE, related_name='testcases')
    output = models.ForeignKey(JsonData, on_delete=models.CASCADE, related_name='testcases')

    config = models.JSONField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(default=5, help_text='high(1) to low(5)')
    version = models.PositiveSmallIntegerField(default=1)
    objects = models.Manager()
    active_objects = TestCaseActiveManager()

    def __str__(self):
        return f"{self.input.name}/{self.name}"


class Category(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH_ADDRESS, unique=True)
    description = models.TextField()

    testcases = models.ManyToManyField(TestCase, related_name='categories')

    def __str__(self):
        return f"{self.name}"


class Suite(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH_ADDRESS, unique=True)
    description = models.TextField()

    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.name}"
