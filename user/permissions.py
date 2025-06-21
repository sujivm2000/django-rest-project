from django.db import models
from rest_framework import permissions

from base.settings import DjangoUtil

settings = DjangoUtil.settings()


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_allowed = super().has_permission(request, view)
        if is_allowed:
            view.request = request
            try:
                view.profile = request.user.profile
            except models.ObjectDoesNotExist:
                return False
        return is_allowed
