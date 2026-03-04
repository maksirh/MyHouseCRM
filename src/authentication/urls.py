from django.urls import path

from .views import AdminLoginView, CabinetLoginView

app_name = "authentication"

urlpatterns = [
    path("cabinet/login/", CabinetLoginView.as_view(), name="cabinet_login"),
    path("adminpanel/login/", AdminLoginView.as_view(), name="admin_login"),
]
