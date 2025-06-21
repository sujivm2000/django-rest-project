from rest_framework.generics import RetrieveAPIView
from django.db.models import Prefetch

from .serializers import (
    TestCaseSerializer,
    CategoryDetailSerializer,
    SuiteDetailSerializer
)
from ..models import Category, TestCase, Suite, Input


class TestCaseDetailView(RetrieveAPIView):
    serializer_class = TestCaseSerializer

    def get_queryset(self):
        queryset = TestCase.objects.select_related(
            'input__json',
            'input__parent',
            'output'
        ).all()
        queryset = queryset.prefetch_related('input__groups')
        return queryset


class CategoryDetailView(RetrieveAPIView):
    serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        queryset = queryset.prefetch_related(
            Prefetch('testcases',
                     queryset=TestCase.objects.select_related(
                         'input__json',
                         'input__parent',
                         'output'
                     ).all().prefetch_related('input__groups')
                     ))
        return queryset


class SuiteDetailView(RetrieveAPIView):
    serializer_class = SuiteDetailSerializer

    def get_queryset(self):
        queryset = Suite.objects.all()
        queryset = queryset.prefetch_related(
            Prefetch('categories__testcases__input'),
            Prefetch('categories__testcases__input__json'),
            Prefetch('categories__testcases__input__parent'),
            Prefetch('categories__testcases__input__groups'),
            Prefetch('categories__testcases__output'),
        )
        return queryset
