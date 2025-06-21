from cryptography.fernet import Fernet
from django.db.models import Q

from base.api.views import (
    BaseListCreateView,
    BaseUpdateDetailView,
    BaseListCreateUpdateView
)
from .serializers import (
    RoleListCreateSerializer,
    RoleDetailSerializer,
    ProfileListCreateUpdateSerializer
)
from ..models.user import User


class RoleListCreateView(BaseListCreateView):
    serializer_class = RoleListCreateSerializer


class RoleUpdateDetailView(BaseUpdateDetailView):
    serializer_class = RoleDetailSerializer


class ProfileListCreateUpdateView(BaseListCreateUpdateView):
    serializer_class = ProfileListCreateUpdateSerializer

    def filter_queryset(self, queryset):
        if self.search_key:
            queryset = queryset.filter(
                Q(user__username__icontains=self.search_key) |
                Q(user__email__icontains=self.search_key)
            )
        return super().filter_queryset(queryset)

    def set_filter_kwargs(self, req_data):
        super().set_filter_kwargs(req_data)
        self.search_key = self.filter_kwargs.pop('search', None)


# class ProfileCreateDetailView(BaseUpdateDetailView):
#     serializer_class = ProfileCreateDetailSerializer
#
#     def post(self, request, *args, **kwargs):
#         if 'id' in kwargs:
#             profile_instance = Profile.objects.get(id=kwargs['id'])
#             role_id = request.data.get('role', None)
#             if 'servers' in request.data:
#                 ser_list = list()
#                 for server in request.data['servers']:
#                     ser_list.append(Server.objects.get(id=server))
#                 if len(ser_list):
#                     profile_instance.servers.clear()
#                     profile_instance.servers.set(ser_list)
#             if role_id:
#                 profile_instance.role = Role.objects.get(id=role_id)
#             profile_instance.save()
#             return_status = status.HTTP_200_OK
#         else:
#             return_status = status.HTTP_400_BAD_REQUEST
#         return Response({}, status=return_status)


# class AuthorizeUserView(BaseCreateView):
#     view_name = 'admin'
#     url_path = '/' + view_name + '/$'
#
#     serializer_class = AuthorizeUserCreateSerializer
#
#     def create(self, request, *args, **kwargs):
#         instance = self.get_user()
#         if not instance:
#             return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)
#
#         password = self.decrypt(self.kwargs.get('password'), self.kwargs.get('pivot'))
#         valid_user = instance.is_staff and instance.is_active and instance.check_password(password)
#         if not valid_user:
#             return Response(data=None, status=status.HTTP_403_FORBIDDEN)
#
#         data = AuthorizeUserDetaiSerializer(instance).data
#         return Response(data=data, status=status.HTTP_200_OK)

    def get_user(self):
        username = self.kwargs.get('email') or ''
        username = username.strip()
        if not username:
            return

        return User.objects.filter(
            Q(email=username) |
            Q(username=username)
        ).first()

    def decrypt(self, chipper, chipper_key):
        if chipper_key:
            fernet = Fernet(chipper_key.encode())
            return fernet.decrypt(chipper.encode()).decode()
        return chipper


# class SSOUserCreateView(BaseCreateView):
#     view_name = 'sso'
#     url_path = '/' + view_name + '/$'
#     serializer_class = SSOUserCreateSerializer
#
#     def create(self, request, *args, **kwargs):
#         instance = self.get_user()
#         if not instance:
#             return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)
#
#         data = AuthorizeUserDetaiSerializer(instance).data
#         return Response(data=data, status=status.HTTP_200_OK)
#
#     def get_user(self):
#         user_email = self.kwargs.get('email') or ''
#         if not user_email:
#             return
#
#         try:
#             return User.objects.get(email=user_email)
#         except User.DoesNotExist:
#             pass
#
#         user_name = user_email
#         if '@' in user_name:
#             user_name = user_name.split('@')[0].strip()
#         try:
#             return User.objects.create(username=user_name, email=user_email)
#         except IntegrityError:
#             pass
