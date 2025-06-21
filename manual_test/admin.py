from django.contrib.admin import register, ModelAdmin
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.html import format_html

from .models import *


class ApiMixin:
    def api(self, obj):
        try:
            url = reverse(self.url_name, args=[obj.id])
            return format_html('<a target="_blank" href="%s">View</a>' % url)
        except:
            return

    api.allow_tags = True


@register(ProjectList)
class ProjectListAdmin(ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_filter = ('name',)
    search_fields = ('name',)


@register(InputGroup)
class InputGroupAdmin(ModelAdmin):
    list_display = ('id', 'type', 'name')
    list_filter = ('type',)
    search_fields = ('name',)


@register(Input)
class InputAdmin(ModelAdmin):
    list_display = ('id', 'testcase_id', 'active', 'project', 'version', 'created_at')
    list_filter = ('active', 'version', 'project')
    search_fields = ('testcase_id', 'project')
    filter_horizontal = ('groups',)
    # raw_id_fields = ('parent',)

    def group_names(self, obj):
        return ','.join([str(o) for o in obj.groups.all()])


@register(StatusHistory)
class StatusHistoryAdmin(ModelAdmin):
    list_display = ('id', 'status_state', 'related_username', 'testcases')
    list_filter = ('status_state',)
    search_fields = ('status_state',)


@register(TestCase)
class TestCaseAdmin(ApiMixin, ModelAdmin):
    list_display = (
        'id', 'name', 'api',  'version', 'created_at')
    list_filter = ('active', 'project', 'environment')
    search_fields = ('name', 'input__name')
    url_name = 'autotest_testcase'
    # filter_horizontal = ('input',)


@register(TestModule)
class TestModuleAdmin(ApiMixin, ModelAdmin):
    list_display = ('id', 'name', 'api', 'description', 'testcase_count')
    search_fields = ('name',)
    filter_horizontal = ('testcases',)
    url_name = 'autotest_testmodule'

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
