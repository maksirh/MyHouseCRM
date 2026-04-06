from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse


def get_user_home_url(user):
    if user.is_superuser:
        return reverse("adminlte:statistic")

    if not user.role:
        return reverse("adminlte:user_profile")

    role = user.role
    if role.has_statistics:
        return reverse("adminlte:statistic")
    if role.has_cashbox:
        return reverse("adminlte:cashbox_list")
    if role.has_receipt:
        return reverse("adminlte:receipt_list")
    if role.has_account_detail:
        return reverse("adminlte:account_list")
    if role.has_apartment:
        return reverse("adminlte:apartment_list")
    if role.has_owner_apartments:
        return reverse("adminlte:owners_list")
    if role.has_message:
        return reverse("adminlte:message_list")
    if role.has_call_master:
        return reverse("adminlte:callmaster_list")
    if role.has_counter:
        return reverse("adminlte:counter_reading_history")

    if role.has_manage_site:
        return reverse("adminlte:edit_main_page")
    if role.has_service:
        return reverse("adminlte:service_edit")
    if role.has_tariffs:
        return reverse("adminlte:tariff_list")
    if role.has_roles:
        return reverse("adminlte:roles_update")
    if role.has_user:
        return reverse("adminlte:users_list")

    return reverse("adminlte:user_profile")


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
