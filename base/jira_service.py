from django.conf import settings
from jira import JIRA


class JiraService:
    """
    Service class to interact with JIRA for creating, updating, and fetching issues.
    """

    def __init__(self):
        """
        Initialize the JIRA connection using settings from Django settings.
        """
        self.jira = JIRA(
            server=settings.JIRA_OPTIONS,
            basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)
        )

    def create_issue(self, project_key, summary, description, issue_type):
        """
        Create a new issue in JIRA.

        :param project_key: The key of the JIRA project.
        :param summary: The summary of the issue.
        :param description: The detailed description of the issue.
        :param issue_type: The type of the issue (e.g., 'Task', 'Bug').
        :return: The created issue object.
        """
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        return self.jira.create_issue(fields=issue_dict)

    def update_issue(self, issue_key, fields):
        """
        Update an existing issue in JIRA.

        :param issue_key: The key of the issue to be updated.
        :param fields: A dictionary of fields to update.
        :return: The updated issue object.
        """
        issue = self.jira.issue(issue_key)  # Fetch the issue to be updated
        issue.update(fields=fields)  # Update the issue with new fields
        return issue

    def get_issues_by_project(self, project_key, jql_str=None):
        """
        Fetch issues filtered by project key and optional JQL query.

        :param project_key: The key of the JIRA project.
        :param jql_str: Additional JQL query string for filtering issues.
        :return: A list of issues matching the query.
        """
        # Default JQL to fetch issues for the specified project
        jql = f'project = {project_key}'
        if jql_str:
            jql += f' AND {jql_str}'  # Add additional JQL filters if provided

        issues = self.jira.search_issues(jql)  # Fetch issues using the JQL query
        return issues
