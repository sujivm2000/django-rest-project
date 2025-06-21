from base.admin import *
from jira_integration.api.views.jira_info import (
    JiraUpdateDetailView,
    JiraTicketUpdateDetailView,
    JiraStatusUpdateDetailView,
    JiraPriorityUpdateDetailView,
    JiraIssueTypeUpdateDetailView,
    JiraRequestTypeUpdateDetailView,
)
from ..models.jira_info import (
    JiraInfo,
    JiraTicketDetail,
    JiraStatus,
    JiraPriority,
    JiraIssueType,
    JiraRequestType
)


@register(JiraInfo)
class JiraAdmin(BaseEntityActiveAdmin):
    api_view = JiraUpdateDetailView
    list_display = BaseEntityActiveAdmin.list_display + [
        'related_user_id', 'api_token'
    ]
    list_filter = BaseEntityActiveAdmin.list_filter + ['related_user_id', 'api_token']
    # filter_horizontal = ('servers',)
    # search_fields = ['user__username', 'role__name']


@register(JiraTicketDetail)
class JiraTicketDetailAdmin(BaseEntityActiveAdmin):
    api_view = JiraTicketUpdateDetailView
    list_display = BaseEntityActiveAdmin.list_display + [
        'jira_id', 'project_key', 'summary', 'description', 'issue_type', 'status'
    ]
    list_filter = BaseEntityActiveAdmin.list_filter + ['jira_id', 'project_key', 'summary', 'description',
                                                       'issue_type', 'status']


@register(JiraStatus)
class JiraStatusAdmin(BaseEntityActiveAdmin):
    api_view = JiraStatusUpdateDetailView
    list_display = BaseEntityActiveAdmin.list_display + [
        'code', 'description'
    ]
    list_filter = BaseEntityActiveAdmin.list_filter + ['code', 'description']


@register(JiraPriority)
class JiraPriorityAdmin(BaseEntityActiveAdmin):
    api_view = JiraPriorityUpdateDetailView
    list_display = BaseEntityActiveAdmin.list_display + [
        'code', 'description'
    ]
    list_filter = BaseEntityActiveAdmin.list_filter + ['code', 'description']


@register(JiraIssueType)
class JiraIssueTypeAdmin(BaseEntityActiveAdmin):
    api_view = JiraIssueTypeUpdateDetailView
    list_display = BaseEntityActiveAdmin.list_display + [
        'code', 'description'
    ]
    list_filter = BaseEntityActiveAdmin.list_filter + ['code', 'description']


@register(JiraRequestType)
class JiraRequestTypeAdmin(BaseEntityActiveAdmin):
    api_view = JiraRequestTypeUpdateDetailView
    list_display = BaseEntityActiveAdmin.list_display + [
        'code', 'description'
    ]
    list_filter = BaseEntityActiveAdmin.list_filter + ['code', 'description']
