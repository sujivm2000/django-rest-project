from jira_integration.api.views.jira_info import (
    JiraListCreateView,
    JiraUpdateDetailView,
    JiraTicketListCreateView,
    JiraTicketUpdateDetailView,
    JiraStatusListCreateView,
    JiraStatusUpdateDetailView,
    JiraPriorityListCreateView,
    JiraPriorityUpdateDetailView,
    JiraIssueTypeListCreateView,
    JiraIssueTypeUpdateDetailView,
    JiraRequestTypeListCreateView,
    JiraRequestTypeUpdateDetailView

)


version = 1

views = [
    JiraListCreateView,
    JiraUpdateDetailView,
    JiraTicketListCreateView,
    JiraTicketUpdateDetailView,
    JiraStatusListCreateView,
    JiraStatusUpdateDetailView,
    JiraPriorityListCreateView,
    JiraPriorityUpdateDetailView,
    JiraIssueTypeListCreateView,
    JiraIssueTypeUpdateDetailView,
    JiraRequestTypeListCreateView,
    JiraRequestTypeUpdateDetailView

]

urlpatterns = []
[urlpatterns.extend(view.urlpatterns(version)) for view in views]
