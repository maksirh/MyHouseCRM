from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import AdminAuthForm


class AdminLoginView(LoginView):
    template_name = "authentication/login.html"
    extra_context = {"is_admin_login": True}
    form_class = AdminAuthForm

    def get_success_url(self):
        return reverse_lazy("adminlte:statistic")


class CabinetLoginView(LoginView):
    template_name = "authentication/login.html"
    extra_context = {"is_admin_login": False}

    def get_success_url(self):
        return reverse_lazy("crm:summary")
