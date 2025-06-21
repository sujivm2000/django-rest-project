from base.api.serializers import (
    BaseModelSerializer
)

from jira_integration.models import (
    JiraInfo,
    JiraTicketDetail,
    JiraStatus,
    JiraPriority,
    JiraIssueType,
    JiraRequestType
)


class JiraListCreateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = JiraInfo
        fields = ['id', 'related_user_id', 'api_token']


class JiraDetailSerializer(JiraListCreateSerializer):
    pass


class JiraTicketListCreateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = JiraTicketDetail


class JiraTicketDetailSerializer(JiraListCreateSerializer):
    pass


class JiraStatusListCreateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = JiraStatus


class JiraStatusDetailSerializer(JiraStatusListCreateSerializer):
    pass


class JiraPriorityListCreateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = JiraPriority


class JiraPriorityDetailSerializer(JiraPriorityListCreateSerializer):
    pass


class JiraIssueTypeListCreateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = JiraIssueType


class JiraIssueTypeDetailSerializer(JiraIssueTypeListCreateSerializer):
    pass


class JiraRequestTypeListCreateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = JiraStatus


class JiraRequestTypeDetailSerializer(JiraRequestTypeListCreateSerializer):
    pass

