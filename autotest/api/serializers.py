from base.api.serializers import serializers, BaseModelSerializer
from ..models import *


class JsonDataSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = JsonData
        fields = ['id', 'data']


class InputGroupSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = InputGroup
        fields = ['id', 'type', 'name']


class InputSerializer(BaseModelSerializer):
    json = JsonDataSerializer()
    parent = serializers.SerializerMethodField()
    groups = InputGroupSerializer(many=True)

    class Meta(BaseModelSerializer.Meta):
        model = Input
        fields = ['id', 'name', 'parent', 'json', 'groups', 'category', 'source']

    def get_parent(self, obj):
        return InputSerializer(obj.parent).data if obj.parent else None


class TestCaseSerializer(BaseModelSerializer):
    input = InputSerializer()
    output = JsonDataSerializer()

    class Meta(BaseModelSerializer.Meta):
        model = TestCase
        fields = ['id', 'name', 'input', 'output', 'config']


class CategoryDetailSerializer(BaseModelSerializer):
    testcases = TestCaseSerializer(many=True)

    class Meta(BaseModelSerializer.Meta):
        model = Category
        fields = ['id', 'name', 'testcases']


class SuiteDetailSerializer(BaseModelSerializer):
    categories = CategoryDetailSerializer(many=True)

    class Meta(BaseModelSerializer.Meta):
        model = Suite
        fields = ['id', 'name', 'categories']
