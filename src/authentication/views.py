from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import AdminAuthForm, CabinetLoginForm


class AdminLoginView(LoginView):
    template_name = "authentication/login.html"
    extra_context = {"is_admin_login": True}
    form_class = AdminAuthForm

    def get_success_url(self):
        return reverse_lazy("adminlte:statistic")


class CabinetLoginView(LoginView):
    template_name = "authentication/login.html"

    form_class = CabinetLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin_login"] = False
        return context

    def get_success_url(self):
        return reverse_lazy("crm:summary")
