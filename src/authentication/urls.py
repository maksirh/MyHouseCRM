from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from .views import AdminLoginView, CabinetLoginView, CabinetRegisterView

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
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="authentication/password_reset_form.html",
            email_template_name="authentication/password_reset_email.html",
            success_url=reverse_lazy("authentication:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="authentication/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="authentication/password_reset_confirm.html",
            success_url=reverse_lazy("authentication:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="authentication/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("cabinet/register/", CabinetRegisterView.as_view(), name="cabinet_register"),
]
