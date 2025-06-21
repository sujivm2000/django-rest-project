from base.api.serializers import serializers, BaseModelSerializer
from ..models import *


class ProjectListSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = ProjectList
        fields = ['id', 'name', 'description']


class TestCaseSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = TestCase
        fields = ['id', 'name','version']


class TestModuleSerializer(BaseModelSerializer):
    testcases = TestCaseSerializer(many=True)

    class Meta(BaseModelSerializer.Meta):
        model = TestModule
        fields = ['id', 'name', 'testcases']


class StatusHistorySerializer(BaseModelSerializer):
    testcases = TestCaseSerializer(many=True)

    class Meta(BaseModelSerializer.Meta):
        model = StatusHistory
        fields = ['id', 'status_state', 'testcases']
