from base.admin import *

from ..models import (
    UserPermission,
    Permission,
    Profile,
    Role
)

from ..api.views import (
    RoleUpdateDetailView,
    # ProfileCreateDetailView,
)


@register(Profile)
class ProfileAdmin(BaseEntityActiveAdmin):
    # api_view = ProfileCreateDetailView
    list_display = BaseEntityActiveAdmin.list_display + [
        'role', 'user', 'type', 'status', 'active'
    ]
    list_filter = BaseEntityActiveAdmin.list_filter + ['status', 'type', 'role']
    # filter_horizontal = ('servers',)
    search_fields = ['user__username', 'role__name']


@register(Role)
class RoleAdmin(BaseEntityAdmin):
    api_view = RoleUpdateDetailView
    list_display = BaseEntityAdmin.list_display + ['name', 'type', 'order']
    list_filter = ('name', )
    search_fields = ['name', 'type']


@register(Permission)
class PermissionAdmin(BaseEntityActiveAdmin):
    list_display = BaseEntityActiveAdmin.list_display + [
        'name', 'ref', 'order', 'active'
    ]
    search_fields = ['name']


@register(UserPermission)
class UserPermissionAdmin(BaseEntityActiveAdmin):
    list_display = BaseEntityActiveAdmin.list_display + [
        'profile_user', 'permission', 'active'
    ]
    list_filter = BaseEntityActiveAdmin.list_filter + [
        'profile__user__username', 'permission'
    ]
    search_fields = [
        'permission__name', 'profile__user__username'
    ]
    raw_id_fields = ('profile', 'permission')

    def profile_user(self, obj):
        return obj.profile.user
