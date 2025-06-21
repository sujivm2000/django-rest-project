import requests
from django.contrib import admin
from django.contrib.admin import register, ModelAdmin
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget

from .models import *


class ApiMixin:
    def api(self, obj):
        try:
            url = reverse(self.url_name, args=[obj.id])
            return format_html('<a target="_blank" href="%s">View</a>' % url)
        except:
            return

    api.allow_tags = True


@register(JsonData)
class JsonDataAdmin(ModelAdmin):
    list_display = ('id', 'data_text')

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    def data_text(self, obj):
        return str(obj.data)[:100]


@register(InputGroup)
class InputGroupAdmin(ModelAdmin):
    list_display = ('id', 'type', 'name')
    list_filter = ('type',)
    search_fields = ('name',)


@register(Input)
class InputAdmin(ModelAdmin):
    list_display = ('id', 'name', 'active', 'app', 'source', 'category', 'version', 'created_at')
    list_filter = ('active', 'version', 'app', 'source', 'category')
    search_fields = ('name', 'parent__name')
    filter_horizontal = ('groups',)
    raw_id_fields = ('parent',)

    def group_names(self, obj):
        return ','.join([str(o) for o in obj.groups.all()])


@register(TestCase)
class TestCaseAdmin(ApiMixin, ModelAdmin):
    list_display = (
        'id', 'name', 'api', 'input', 'description', 'active', 'app', 'source', 'category', 'priority', 'version',
        'created_at')
    list_filter = ('active', 'priority', 'version', 'app', 'source', 'category')
    search_fields = ('name', 'input__name')
    url_name = 'autotest_testcase'
    raw_id_fields = ('input',)


@register(Category)
class CategoryAdmin(ApiMixin, ModelAdmin):
    list_display = ('id', 'name', 'api', 'description', 'testcase_count')
    search_fields = ('name',)
    filter_horizontal = ('testcases',)
    url_name = 'autotest_category'

    def testcase_count(self, obj):
        return obj.testcases.count()

    def get_queryset(self, queryset):
        queryset = super().get_queryset(queryset)

        queryset = queryset.prefetch_related(
            Prefetch(
                'testcases',
                queryset=TestCase.objects.select_related('input')
            ))
        return queryset


@register(Suite)
class SuiteAdmin(ApiMixin, ModelAdmin):
    list_display = ('id', 'name', 'api', 'description', 'category_names', 'category_count')
    search_fields = ('name',)
    filter_horizontal = ('categories',)
    url_name = 'autotest_suite'

    def category_names(self, obj):
        return ','.join([str(o) for o in obj.categories.all()])

    def category_count(self, obj):
        return obj.categories.count()
