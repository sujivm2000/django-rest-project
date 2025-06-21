from base.api.views import (
    BaseListCreateView,
    BaseUpdateDetailView
)

from jira_integration.api.serializers.jira_info import (
    JiraListCreateSerializer,
    JiraDetailSerializer,
    JiraTicketListCreateSerializer,
    JiraTicketDetailSerializer,
    JiraStatusListCreateSerializer,
    JiraStatusDetailSerializer,
    JiraPriorityListCreateSerializer,
    JiraPriorityDetailSerializer,
    JiraIssueTypeListCreateSerializer,
    JiraIssueTypeDetailSerializer,
    JiraRequestTypeListCreateSerializer,
    JiraRequestTypeDetailSerializer
)


class JiraListCreateView(BaseListCreateView):
    serializer_class = JiraListCreateSerializer


class JiraUpdateDetailView(BaseUpdateDetailView):
    serializer_class = JiraDetailSerializer


class JiraTicketListCreateView(BaseListCreateView):
    serializer_class = JiraTicketListCreateSerializer


class JiraTicketUpdateDetailView(BaseUpdateDetailView):
    serializer_class = JiraTicketDetailSerializer


class JiraStatusListCreateView(BaseListCreateView):
    serializer_class = JiraStatusListCreateSerializer


class JiraStatusUpdateDetailView(BaseUpdateDetailView):
    serializer_class = JiraStatusDetailSerializer


class JiraPriorityListCreateView(BaseListCreateView):
    serializer_class = JiraPriorityListCreateSerializer


class JiraPriorityUpdateDetailView(BaseUpdateDetailView):
    serializer_class = JiraPriorityDetailSerializer


class JiraIssueTypeListCreateView(BaseListCreateView):
    serializer_class = JiraIssueTypeListCreateSerializer


class JiraIssueTypeUpdateDetailView(BaseUpdateDetailView):
    serializer_class = JiraIssueTypeDetailSerializer


class JiraRequestTypeListCreateView(BaseListCreateView):
    serializer_class = JiraRequestTypeListCreateSerializer


class JiraRequestTypeUpdateDetailView(BaseUpdateDetailView):
    serializer_class = JiraRequestTypeDetailSerializer
