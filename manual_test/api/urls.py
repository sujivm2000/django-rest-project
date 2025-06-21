from django.urls import path

from .views import *

urlpatterns = [
    path('v1/autotest/projectlist/<int:pk>/', ProjectListView.as_view(), name='manual_projectlist'),
    path('v1/autotest/testcase/<int:pk>/', TestCaseDetailView.as_view(), name='manual_testcase'),
    path('v1/autotest/testmodule/<int:pk>/', TestModuleView.as_view(), name='manual_testmodule'),
    path('v1/autotest/statushistory/<int:pk>/', TestModuleView.as_view(), name='manual_statushistory'),

]
