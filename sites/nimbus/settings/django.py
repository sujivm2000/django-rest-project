import os
import json

os.environ['APP_LIST'] = str([
                            'user',
                            'autotest',
                            'manual_test',
                            'cricket',
                            'jira_integration'
                        ])

try:
    from base.settings.django import *
except:
    from base.settings.django import *

API_APP_LIST = [
                'user',
                'autotest',
                'manual_test',
                'cricket',
                'jira_integration'
            ]

INSTALLED_APPS += ['base', 'django_json_widget', 'django_better_admin_arrayfield',]

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'user.permissions.IsAuthenticated'
]

ALLOWED_CONTENT_TYPES = [
    'application/pdf',
    'application/zip',
    # Add more content types as needed
]

JIRA_OPTIONS = {
    'server': 'https://your-jira-server'
}
JIRA_EMAIL = 'your-jira-username'
JIRA_API_TOKEN = 'your-jira-password'

os.environ['AUTOTEST_APP_LIST'] = json.dumps({
    "beaumont": "Beaumont",
    "mondiale": "Mondiale"
})

os.environ['AUTOTEST_CATEGORY_LIST'] = json.dumps({
    "beaumont.smith_and_riley": "SmithAndRiley",
    "beaumont.toll": "TollGlobal",
    "beaumont.team": "TeamTransport",
    "mondiale.ex_word": "ExWork",
    "mondiale.detention": "Detention",
    "mondiale.Domestic": "SeaDomestic",
})

