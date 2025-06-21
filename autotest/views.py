from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework.generics import ListCreateAPIView

from .models import TestCase
from .serializers import DownloadTestCaseSerializer


class DownloadTestCaseView(XLSXFileMixin, ListCreateAPIView):
    serializer_class = DownloadTestCaseSerializer
    renderer_classes = [XLSXRenderer]

    column_header = {
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': '70ad47'
            },
            'alignment': {
                'wrapText': True
            }
        }
    }
    body = {
        'style': {
            'alignment': {
                'wrapText': True
            }
        }
    }

    def get_filename(self):
        filename = 'testcases.xlsx'
        return filename

    def get_queryset(self):
        queryset = TestCase.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = TestCase.objects.filter(parent__name=name)
        return queryset
