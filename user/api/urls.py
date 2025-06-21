from .views import (
    RoleUpdateDetailView,
    RoleListCreateView,

    ProfileListCreateUpdateView,

)

version = 1

views = [
    RoleListCreateView,
    RoleUpdateDetailView,

    ProfileListCreateUpdateView,

]

urlpatterns = []
[urlpatterns.extend(view.urlpatterns(version)) for view in views]
