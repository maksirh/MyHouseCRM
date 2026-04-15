from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from src.crm.models import PersonalAccount

from .forms import AdminAuthForm, CabinetLoginForm, CabinetRegistrationForm


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


class CabinetRegisterView(CreateView):
    form_class = CabinetRegistrationForm
    template_name = "authentication/register.html"
    success_url = reverse_lazy("crm:summary")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()

        acc_num = form.cleaned_data["account_number"]
        account = (
            PersonalAccount.objects.filter(number=acc_num)
            .select_related("apartment")
            .first()
        )

        if account and hasattr(account, "apartment") and account.apartment:
            account.apartment.owner = user
            account.apartment.save()

        login(self.request, user)

        return super().form_valid(form)
