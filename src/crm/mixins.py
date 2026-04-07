from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class CabinetLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("authentication:cabinet_login")
