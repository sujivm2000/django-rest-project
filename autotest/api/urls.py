from django.urls import path

from .views import *

urlpatterns = [
    path('v1/autotest/testcase/<int:pk>/', TestCaseDetailView.as_view(), name='autotest_testcase'),
    path('v1/autotest/category/<int:pk>/', CategoryDetailView.as_view(), name='autotest_category'),
    path('v1/autotest/suite/<int:pk>/', SuiteDetailView.as_view(), name='autotest_suite'),
]
