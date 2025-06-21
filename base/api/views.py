import logging
import traceback
from urllib.parse import unquote
from rest_framework import status
from django.core.exceptions import FieldError, ValidationError
from django.http import Http404
from django.urls import path
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import (
    GenericAPIView, CreateAPIView,
    ListAPIView, ListCreateAPIView,
    RetrieveAPIView,DestroyAPIView
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST
)
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.views import exception_handler as drf_exception_handler

from ..decorators import authorize_user

log = logging.getLogger(__name__)


def url_prefix(version):
    return r'v%d/' % version


def exception_handler(exc, *args, **kwargs):
    resp = drf_exception_handler(exc, *args, **kwargs)
    if not resp:
        if isinstance(exc, FieldError):
            log.error(exc)
            resp = Response(status=HTTP_400_BAD_REQUEST)
    return resp


class StandardCursorPagination(CursorPagination):
    ordering = 'id'
    page_size_query_param = 'page_size'
    page_size = 25
    max_page_size = 100


class StandardPageNumberPagination(PageNumberPagination):
    ordering = 'id'
    page_size_query_param = 'page_size'
    page_size = 50
    max_page_size = 100


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class BaseAuthentication:
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_required_permissions(self):
        perm_dict = {
            'GET': [
            ],
            'POST': [
            ],
        }
        return perm_dict[self.request.method]


class UrlMixin(BaseAuthentication):
    app_label = None

    @classmethod
    def model(cls):
        return cls.serializer_class.Meta.model

    @classmethod
    def get_api_name(cls, context_prefix=''):
        model_meta = cls.model()._meta
        app_label = cls.app_label or model_meta.app_label
        return '%s/%s%s' % (app_label, context_prefix, model_meta.model_name)

    @classmethod
    def get_url_path(cls):
        return cls.url_path

    @classmethod
    def get_url_name(cls, name=None, context_prefix=''):
        model_meta = cls.model()._meta
        app_label = cls.app_label or model_meta.app_label
        name = name or cls.view_name
        return app_label + '_' + \
            context_prefix + \
            model_meta.model_name + \
            ('_' + name if name else name)

    @classmethod
    def get_url(cls, *args):
        return reverse(cls.get_url_name(), args=args)

    @classmethod
    def urlpatterns(cls, version):
        name = cls.get_url_name()
        prefix = url_prefix(version) + cls.get_api_name() + cls.get_url_path()
        return [
            path(prefix, cls.as_view(), name=name),
        ]


class ContextModelMixin:
    context_lookup_field = 'id'
    context_url_kwarg = 'cid'
    context_model = None

    @classmethod
    def get_api_name(cls):
        context_prefix = '%s/(?P<%s>[\d]+)/' % (
            cls.context_model._meta.model_name, cls.context_url_kwarg
        ) if cls.context_model else ''
        return super().get_api_name(context_prefix=context_prefix)

    @classmethod
    def get_url_name(cls, name=None):
        context_prefix = (cls.context_model._meta.model_name + '_') if cls.context_model else ''
        return super().get_url_name(context_prefix=context_prefix)

    def set_context_instance(self):
        self.context_instance = None
        if self.context_model:
            try:
                queryset = self.context_model.objects.all()
                self.context_instance = self.filter_context_queryset(queryset).get()
            except Exception as error:
                raise Http404

    def filter_context_queryset(self, queryset):
        return queryset.filter(**{
            self.context_lookup_field: self.kwargs[self.context_url_kwarg]
        })


class EntityMixin:
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        self.kwargs[self.lookup_url_kwarg] = self.kwargs.get(self.lookup_url_kwarg, '')
        if isinstance(self.kwargs[self.lookup_url_kwarg], str):
            self.kwargs[self.lookup_url_kwarg] = unquote(self.kwargs.get(self.lookup_url_kwarg, ''))

        objs = self.get_manager()
        if hasattr(self, 'filter_kwargs'):
            objs = objs.filter(**self.filter_kwargs)
        return objs.all()

    def get_manager(self):
        return self.model().objects

    def get_key(self):
        return self.kwargs.get(self.lookup_url_kwarg, '')

    def set_kwargs(self, req_data):
        self.kwargs.update(req_data.items())

    def set_filter_kwargs(self, req_data):
        self.filter_kwargs = {}
        for key, val in req_data.items():
            if val and key not in ('csrfmiddlewaretoken', 'cursor', 'page', 'format'):
                self.filter_kwargs[key] = val


class BaseActiveManagerMixin:
    def get_manager(self):
        return self.model().active_objects


class CreateUpdateMixin:
    def update_or_create(self, model, data, unique_key_kwargs=None):
        if not unique_key_kwargs:
            unique_key_kwargs, defaults = self.get_key_and_defaults(model, data)
        else:
            defaults = data
        return model.objects.update_or_create(**unique_key_kwargs, defaults=defaults)

    def get_unique_together_field_names(self, model):
        return getattr(model._meta, 'unique_together', (('id',),))[0]

    def get_key_and_defaults(self, model, data):
        field_kwargs = {}

        # get field name from unique together in model
        for field_name in self.get_unique_together_field_names(model):
            field = model._meta.get_field(field_name)

            key = field_name + '_id' if field.is_relation else field_name
            field_kwargs[key] = data.pop(field_name) if field.is_relation else data[field_name]
        return field_kwargs, data


@method_decorator(authorize_user, name="dispatch")
class BaseCreateView(ContextModelMixin, UrlMixin, EntityMixin, CreateAPIView):
    url_path = '/'
    view_name = 'create'

    def post(self, request, *args, **kwargs):
        self.set_kwargs(request.data)
        self.set_context_instance()
        resp = self.create(request, *args, **kwargs)
        log.info('%s %s %s: %s' % (request.method, request.path, request.data, resp.status_code))
        return resp


@method_decorator(authorize_user, name="dispatch")
class BaseCreateUpdateBulkView(ContextModelMixin, UrlMixin, CreateUpdateMixin, CreateAPIView):
    url_path = '/'
    view_name = 'create_update_bulk'

    def get_queryset(self):
        objs = self.get_manager()
        return objs.all()

    def get_manager(self):
        return self.model().objects

    def post(self, request, *args, **kwargs):
        self.set_context_instance()
        self.set_kwargs(kwargs)
        resp_data = []
        for item_data in request.data:
            if not item_data:
                continue
            status_dict = {}
            try:
                item, is_created = self.create_or_update_item(item_data)
                status_dict['status'] = ('Created' if is_created else 'Updated') if item else 'Ignored'
                status_dict['id'] = item.id if item else None
            except Exception as e:
                log.error("UnKnown Error: %s", e)
                status_dict['status'] = 'error: %s' % str(e)
                log.error(traceback, item_data)
            finally:
                resp_data.append(status_dict)
        resp = Response(self.get_response_data(resp_data))
        log.info('%s %s %s' % (request.method, request.path, resp_data))
        return resp

    def set_kwargs(self, req_data):
        self.src_id = req_data.get('src_id')

    def get_response_data(self, resp_data):
        return resp_data

    def create_or_update_item(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid()
        model = self.get_serializer_class().Meta.model
        id = data.pop('id', None)
        kwargs = {'unique_key_kwargs': {'id': id}} if id else {}
        instance, is_created = self.update_or_create(model, data, **kwargs)
        return instance, is_created


@method_decorator(authorize_user, name="dispatch")
class BaseListView(ContextModelMixin, UrlMixin, EntityMixin, ListAPIView):
    url_path = '/'
    view_name = 'list'

    def get(self, request, *args, **kwargs):
        self.set_filter_kwargs(request.query_params)
        self.set_kwargs(kwargs)
        self.set_context_instance()
        log.info('%s %s %s ' % (request.method, request.path, dict(request.query_params)))
        return self.list(request, *args, **kwargs)

    def set_kwargs(self, req_data):
        return req_data


@method_decorator(authorize_user, name="dispatch")
class BaseListCreateView(ContextModelMixin, UrlMixin, EntityMixin, ListCreateAPIView):
    url_path = '/'
    view_name = 'list_create'

    def get(self, request, *args, **kwargs):
        self.set_filter_kwargs(request.query_params)
        self.set_context_instance()
        log.info('%s %s %s ' % (request.method, request.path, dict(request.query_params)))
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.set_context_instance()
        self.set_kwargs(request.data)
        resp = self.create(request, *args, **kwargs)
        log.info('%s %s %s: %s' % (request.method, request.path, request.data, resp.status_code))
        return resp


@method_decorator(authorize_user, name="dispatch")
class BaseListCreateUpdateView(UpdateModelMixin, BaseListCreateView):
    view_name = 'list_create_update'

    def post(self, request, *args, **kwargs):
        self.set_kwargs(request.data)
        self.set_context_instance()
        try:
            resp = self.update(request, *args, **kwargs)
        except Http404:
            resp = self.create(request, *args, **kwargs)
        log.info('%s %s %s: %s' % (request.method, request.path, request.data, resp.status_code))
        return resp


@method_decorator(authorize_user, name="dispatch")
class BaseDetailView(ContextModelMixin, UrlMixin, EntityMixin, RetrieveAPIView):
    url_path = '/<int:id>/'
    view_name = 'detail'

    @classmethod
    def urlpatterns(cls, version):
        return format_suffix_patterns(super().urlpatterns(version))

    def retrieve(self, request, *args, **kwargs):
        self.set_filter_kwargs(request.query_params)
        self.set_context_instance()
        log.info('%s %s %s ' % (request.method, request.path, dict(request.query_params)))
        return super().retrieve(request, *args, **kwargs)


@method_decorator(authorize_user, name="dispatch")
class BaseUpdateDetailView(UpdateModelMixin, BaseDetailView):
    view_name = 'update_detail'

    def post(self, request, *args, **kwargs):
        self.set_context_instance()
        resp = self.partial_update(request, *args, **kwargs)

        log.info('%s %s %s: %s' % (request.method, request.path, dict(request.data), resp.status_code))
        return resp


@method_decorator(authorize_user, name="dispatch")
class BaseSummaryView(ContextModelMixin, UrlMixin, GenericAPIView):
    view_name = 'summary'
    url_path = '/' + view_name + '/'

    def get(self, request, *args, **kwargs):
        self.set_context_instance()
        log.info('%s %s %s ' % (request.method, request.path, dict(request.query_params)))
        data = self.summary(request, *args, **kwargs)
        return Response(data)


@method_decorator(authorize_user, name="dispatch")
class BaseDiffView(UrlMixin, GenericAPIView):
    view_name = 'diff'
    url_path = '/' + view_name + '/'

    def get(self, request, *args, **kwargs):
        log.info('%s %s %s ' % (request.method, request.path, dict(request.query_params)))
        data = self.diff(request, *args, **kwargs)

        return Response(data)

    def get_queryset(self):
        return


@method_decorator(authorize_user, name="dispatch")
class BaseCloneCreateView(ContextModelMixin, UrlMixin, EntityMixin, CreateUpdateMixin, GenericAPIView):
    url_path = 'clone/(?P<src_id>[\d]+)/'
    view_name = 'clone'

    @classmethod
    def get_url_name(cls, name=None):
        url_name = super().get_url_name(name=None)
        url_name = url_name.replace(f'client_{cls.view_name}', cls.view_name)
        return url_name

    @classmethod
    def get_api_name(cls):
        api_name = super().get_api_name()
        return ''.join(api_name.rsplit(cls.context_model._meta.model_name, 1)[:-1])

    def get(self, request, *args, **kwargs):
        status = None
        self.set_kwargs(kwargs)
        self.set_filter_kwargs(request.query_params)
        self.set_context_instance()
        return self.clone(request, *args, **kwargs)

    def set_kwargs(self, req_data):
        self.src_id = req_data.get('src_id')

    def clone_data(self, serializer_class, data):
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return instance

    def clone_data_list(self, model, data_list):
        ll = list()
        for data in data_list:
            obj, created = self.update_or_create(model, data)
            ll.append((obj, created))
        return ll

@method_decorator(authorize_user, name="destroy")
class BaseDestroyView(ContextModelMixin, UrlMixin, EntityMixin, DestroyAPIView):
    url_path = '/delete/<int:id>/'
    view_name = 'delete'

    def delete(self, request, *args, **kwargs):
        self.set_context_instance()
        try:
            resp = self.destroy(request, *args, **kwargs)
        except ValidationError as vl_err:
            return Response(data=vl_err.message, status=status.HTTP_400_BAD_REQUEST)
        log.info('%s %s %s: %s' % (request.method, request.path, dict(request.data), resp.status_code))
        return Response(data=resp.data, status=status.HTTP_200_OK)