from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import AdminLoginView, CabinetLoginView

app_name = "authentication"

urlpatterns = [
    path("cabinet/login/", CabinetLoginView.as_view(), name="cabinet_login"),
    path("adminpanel/login/", AdminLoginView.as_view(), name="admin_login"),
    path(
        "adminpanel/logout/",
        LogoutView.as_view(next_page="authentication:admin_login"),
        name="admin_logout",
    ),
    path(
        "cabinet/logout/",
        LogoutView.as_view(next_page="authentication:cabinet_login"),
        name="cabinet_logout",
    ),
]
