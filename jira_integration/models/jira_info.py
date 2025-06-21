from django.contrib.auth.models import User

from base.models import (
    models,
    BaseActiveModel
)

ISSUE_TYPE_CHOICES = [
    "Task",
    "Bug",
    "Story",
]
STATUS_TASK, STATUS_BUG, STATUS_STORY = ISSUE_TYPE_CHOICES

PRIORITY_CHOICES = [
    "High",
    "Medium",
    "Low",
]
STATUS_HIGH, STATUS_MEDIUM, STATUS_LOW = PRIORITY_CHOICES

REQUEST_TYPE_CHOICES = [
    "New Request",
    "Re Issue Request"
]
STATUS_NEW_REQUEST, STATUS_RE_ISSUE_REQUEST = REQUEST_TYPE_CHOICES

STATUS_CHOICES = [
    "To Do",
    "On Hold",
    "In Progress",
    "Testing",
    "Done"
]
STATUS_TO_DO, STATUS_ON_HOLD, STATUS_IN_PROGRESS, STATUS_TESTING, STATUS_DONE = STATUS_CHOICES


class JiraInfo(BaseActiveModel):
    related_user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                                        related_name='jira_user_info')
    api_token = models.CharField(max_length=500, null=True, blank=True)

    class Meta(BaseActiveModel.Meta):
        pass


class JiraTicketDetail(BaseActiveModel):
    jira_id = models.ForeignKey(JiraInfo, on_delete=models.CASCADE, null=False, blank=False,
                                related_name='jira_ticket_detail')
    project_key = models.CharField(max_length=50, null=False, blank=False)
    summary = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    issue_type = models.CharField(max_length=50,
                                  choices=((s, s.upper()) for s in ISSUE_TYPE_CHOICES),
                                  default=STATUS_TASK)
    uuid = models.CharField(max_length=50, null=True, blank=True)
    issue_key = models.CharField(max_length=50, null=True, blank=True)
    request_type = models.CharField(max_length=50,
                                    choices=((s, s.upper()) for s in REQUEST_TYPE_CHOICES),
                                    default=STATUS_NEW_REQUEST)
    priority = models.CharField(max_length=50,
                                choices=((s, s.upper()) for s in PRIORITY_CHOICES),
                                default=STATUS_HIGH)
    status = models.CharField(max_length=50,
                              choices=((s, s.upper()) for s in STATUS_CHOICES),
                              default=STATUS_TO_DO)
    assign_to = models.CharField(max_length=50, null=True, blank=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)

    class Meta(BaseActiveModel.Meta):
        pass


class JiraStatus(BaseActiveModel):
    code = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=50, null=False, blank=False)

    class Meta(BaseActiveModel.Meta):
        pass


class JiraIssueType(BaseActiveModel):
    code = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=50, null=False, blank=False)

    class Meta(BaseActiveModel.Meta):
        pass


class JiraRequestType(BaseActiveModel):
    code = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=50, null=False, blank=False)

    class Meta(BaseActiveModel.Meta):
        pass


class JiraPriority(BaseActiveModel):
    code = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=50, null=False, blank=False)

    class Meta(BaseActiveModel.Meta):
        pass
