from base.api.serializers import (
    BaseModelSerializer,
    BaseDetailSerializer
)

from ..models import (
    Role, Profile,
    User, Permission
)


class RoleListCreateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Role
        fields = ['id', 'name', 'type']


class RoleDetailSerializer(RoleListCreateSerializer):
    pass


class UserDetailSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email']


class ProfileRoleDetailSerializer(RoleDetailSerializer):
    class Meta(RoleDetailSerializer.Meta):
        pass


class ProfileUserDetailSerializer(UserDetailSerializer):
    class Meta(UserDetailSerializer.Meta):
        pass


class PermissionDetailSerializer(BaseDetailSerializer):
    class Meta(BaseDetailSerializer.Meta):
        model = Permission
        fields = ['id', 'name']


class ProfileListCreateUpdateSerializer(BaseModelSerializer):
    role = ProfileRoleDetailSerializer()
    user = ProfileUserDetailSerializer()

    class Meta(BaseModelSerializer.Meta):
        model = Profile
        fields = ['id', 'type', 'status', 'mobile', 'role', 'user']


class AuthorizeUserCreateSerializer(BaseDetailSerializer):
    class Meta(BaseDetailSerializer.Meta):
        model = User
        fields = (
            'password', 'email'
        )


class SSOUserCreateSerializer(AuthorizeUserCreateSerializer):
    class Meta(AuthorizeUserCreateSerializer.Meta):
        fields = ('email', )
