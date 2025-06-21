from django.conf.urls import include, static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from ..settings import DjangoUtil;
from ..utils import import_module_var

settings = DjangoUtil.settings()

from ..views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('openapi/', get_schema_view(
        title="DreamBig Api Service",
        description="API developers hpoing to use our service"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

]

for app in settings.APP_LIST:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', home),
        path('openapi/', get_schema_view(
            title="DreamBig Api Service",
            description="API developers hpoing to use our service"
        ), name='openapi-schema'),
        path('swagger-ui/', TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ), name='swagger-ui'),

    ]
    prefix = import_module_var(app + '.URL_PREFIX', app)
    try:
        if prefix:
            prefix += '/'
        urlpatterns.append(
            path(prefix, include(app + '.urls'))
        )
    except ImportError:
        pass


def get_urlpatterns(api_prefix=''):
    patterns = []

    for app in settings.API_APP_LIST:
        try:
            patterns.append(
                path(api_prefix, include(app + '.api.urls'))
            )
        except ModuleNotFoundError as err:
            print(f'failed to load app api urls: {str(err)}')

    return patterns


urlpatterns += get_urlpatterns()


def add_debug_urlpatterns(urlpatterns):
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    return urlpatterns


if settings.DEBUG:
    urlpatterns = add_debug_urlpatterns(urlpatterns)

# urlpatterns += [
#     re_path(r'(?:login|dashboard|Configuration|SkuConfiguration|UserList|Detail|SkuNotes|CompareClients|home|valuechain2|valuechain)', home)
# ]
