from django.urls import path
from .views import DownloadTestCaseView

urlpatterns = [
    path('download/', DownloadTestCaseView.as_view(), name='download-testcase'),
]