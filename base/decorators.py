from django.core.exceptions import PermissionDenied


def authorize_user(view_func):
    def wrapper(request, *args, **kwargs):
        # if request.user.is_anonymous:
        #     raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper
