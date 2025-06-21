import json
from django.contrib.auth.models import User

from base.models import MAX_LENGTH_NAME, MAX_LENGTH_ADDRESS, BaseModel, BaseTimeModel
from django.db import models


class JsonData(BaseModel):
    data = models.JSONField()

    def __str__(self):
        return str(self.id)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class ProjectList(BaseTimeModel):
    name = models.CharField(max_length=MAX_LENGTH_NAME, null=True, blank=True)
    description = models.CharField(max_length=MAX_LENGTH_NAME, null=True, blank=True)

    class Meta(BaseTimeModel.Meta):
        pass


class BaseCategory(BaseTimeModel):
    ENVIRONMENT_CHOICES = [(k, v) for k, v in (json.loads('{"Test": "TEST", "Development": "DEVELOPMENT",'
                                                          '"Production": "PRODUCTION"}')).items()]

    project = models.ForeignKey(ProjectList, on_delete=models.CASCADE, null=False, blank=False)

    environment = models.CharField(max_length=MAX_LENGTH_NAME, null=True, blank=True, choices=ENVIRONMENT_CHOICES)

    class Meta(BaseTimeModel.Meta):
        abstract = True


class InputGroup(BaseModel):
    type = models.CharField(max_length=MAX_LENGTH_NAME, help_text='project name, testmodule etc.,')
    name = models.CharField(max_length=MAX_LENGTH_NAME)

    class Meta(BaseModel.Meta):
        unique_together = ('type', 'name',)

    def __str__(self):
        return f"{self.type}/{self.name}"


class Input(BaseCategory):
    testcase_id = models.CharField(max_length=MAX_LENGTH_ADDRESS, null=False, blank=False,
                                   help_text='TC_ID_01')
    scenario = models.CharField(max_length=MAX_LENGTH_ADDRESS, null=False, blank=False)
    cases = models.TextField(max_length=MAX_LENGTH_ADDRESS, null=False, blank=False,
                             help_text="""
        Given external user is in Login page
        When external user enters <Email> and <Password>
        Then external user should login to the page
        """)
    test_data = models.TextField(max_length=MAX_LENGTH_ADDRESS, null=True, blank=True)
    actual_result = models.CharField(max_length=MAX_LENGTH_ADDRESS, null=False, blank=False)

    STATUS_CHOICES = [(k, v) for k, v in (json.loads('{"Pass": "PASS", "Failed": "FAILED",'
                                                     '"Running": "RUNNING", "Stopped": "STOPPED"}')).items()]
    status = models.CharField(max_length=MAX_LENGTH_NAME, choices=STATUS_CHOICES, default=None)

    developer_status = models.TextField(null=True, blank=True)
    retest_status = models.CharField(max_length=MAX_LENGTH_NAME, choices=STATUS_CHOICES, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=False)
    version = models.PositiveSmallIntegerField(default=1)

    groups = models.ManyToManyField(InputGroup, blank=True)

    objects = models.Manager()

    active_objects = ActiveManager()

    def __str__(self):
        return f"{self.testcase_id}"


class TestCaseActiveManager(ActiveManager):
    def get_queryset(self):
        return super().get_queryset().filter(input__active=True)


class TestCase(BaseCategory):
    name = models.CharField(max_length=MAX_LENGTH_ADDRESS, null=False, blank=False)
    input = models.ForeignKey(Input, on_delete=models.CASCADE, related_name='testcases')
    active = models.BooleanField(default=False)
    version = models.PositiveSmallIntegerField(default=1)
    objects = models.Manager()
    active_objects = TestCaseActiveManager()

    def __str__(self):
        return f"{self.name}"


class TestModule(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH_ADDRESS, unique=True)
    description = models.TextField()

    testcases = models.ManyToManyField(TestCase, related_name='testmodules')

    def __str__(self):
        return f"{self.name}"


class StatusHistory(BaseModel):
    status_state = models.CharField(max_length=MAX_LENGTH_ADDRESS)
    related_username = models.ForeignKey(User, on_delete=models.CASCADE)
    testcases = models.ForeignKey(TestCase, on_delete=models.CASCADE)

    class Meta(BaseModel.Meta):
        pass

    def __str__(self):
        return f"{self.status_state}/{self.related_username}"
