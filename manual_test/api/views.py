from rest_framework.generics import RetrieveAPIView
from django.db.models import Prefetch

from .serializers import (
    TestCaseSerializer,
    TestModuleSerializer,
    ProjectListSerializer,
    StatusHistorySerializer
)
from ..models import TestCase, TestModule


class TestCaseDetailView(RetrieveAPIView):
    serializer_class = TestCaseSerializer

    def get_queryset(self):
        queryset = TestCase.objects.select_related(
            'input__json',
            'input__parent',
        ).all()
        queryset = queryset.prefetch_related('input__groups')
        return queryset


class TestModuleView(RetrieveAPIView):
    serializer_class = TestModuleSerializer

    def get_queryset(self):
        queryset = TestModule.objects.all()
        queryset = queryset.prefetch_related(
            Prefetch('testcases',
                     queryset=TestCase.objects.select_related(
                         'input__json',
                         'input__parent',
                         'output'
                     ).all().prefetch_related('input__groups')
                     ))
        return queryset


class ProjectListView(RetrieveAPIView):
    serializer_class = ProjectListSerializer


class StatusHistoryView(RetrieveAPIView):
    serializer_class = StatusHistorySerializer
