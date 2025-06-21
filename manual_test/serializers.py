from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import TestCase


class DownloadTestCaseSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()
    input = serializers.SerializerMethodField()

    class Meta:
        model = TestCase
        fields = ('name', 'version', 'input', 'output', 'active', 'priority',)

    def get_name(self, obj):
        return obj.parent.name

    def get_version(self, obj):
        return obj.parent.version

    def get_input(self, obj):
        return obj.input.json

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.update({'input': [response.get('input')]})
        response.update({'output': [response.get('output')]})
        return response
