from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse


def get_user_home_url(user):
    if user.is_superuser:
        return reverse("adminlte:statistic")

    if not getattr(user, "role", None):
        return reverse("adminlte:user_profile")

    role_urls = {
        "has_statistics": "adminlte:statistic",
        "has_cashbox": "adminlte:cashbox_list",
        "has_receipt": "adminlte:receipt_list",
        "has_account_detail": "adminlte:account_list",
        "has_apartment": "adminlte:apartment_list",
        "has_owner_apartments": "adminlte:owners_list",
        "has_message": "adminlte:message_list",
        "has_call_master": "adminlte:callmaster_list",
        "has_counter": "adminlte:counter_reading_history",
        "has_manage_site": "adminlte:edit_main_page",
        "has_service": "adminlte:service_edit",
        "has_tariffs": "adminlte:tariff_list",
        "has_roles": "adminlte:roles_update",
        "has_user": "adminlte:users_list",
    }

    url_name = next(
        (url for attr, url in role_urls.items() if getattr(user.role, attr, False)),
        "adminlte:user_profile",
    )

    return reverse(url_name)


class RolePermissionMixin(UserPassesTestMixin):
    required_permission = None

    def test_func(self):
        user = self.request.user

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        has_permission = getattr(user.role, self.required_permission, False)

        return has_permission

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request, "У вас немає прав для перегляду цієї сторінки."
            )
            return redirect(get_user_home_url(self.request.user))

        return super().handle_no_permission()
