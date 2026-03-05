from django.urls import path

from .views import (
    AboutUsPageView,
    ContactPageView,
    MainPageView,
    RoleCreateView,
    RoleDeleteView,
    RolesUpdateView,
    ServicePageView,
    StatisticPageView,
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserEditView,
    UserListView,
    UserProfileView,
)

app_name = "adminlte"

urlpatterns = [
    path("", StatisticPageView.as_view(), name="statistic"),
    path("managesite/mainpage", MainPageView.as_view(), name="edit_main_page"),
    path("managesite/aboutus", AboutUsPageView.as_view(), name="edit_about_us_page"),
    path("managesite/services", ServicePageView.as_view(), name="edit_service_page"),
    path("managesite/contacts", ContactPageView.as_view(), name="contacts_edit"),
    path("settings/", RolesUpdateView.as_view(), name="roles_update"),
    path("roles/create/", RoleCreateView.as_view(), name="role_create"),
    path("roles/delete/<int:pk>", RoleDeleteView.as_view(), name="role_delete"),
    path("user/edit/<int:pk>", UserEditView.as_view(), name="user_edit"),
    path("user/create/", UserCreateView.as_view(), name="user_create"),
    path("user/list/", UserListView.as_view(), name="users_list"),
    path("user/profile", UserProfileView.as_view(), name="user_profile"),
    path("user/detail/<int:pk>", UserDetailView.as_view(), name="user_detail"),
    path("user/delete/<int:pk>", UserDeleteView.as_view(), name="user_delete"),
]
