from django.urls import path

from .views import MainPageView, StatisticPageView

app_name = "adminlte"

urlpatterns = [
    path("", StatisticPageView.as_view(), name="statistic"),
    path("managesite/mainpage", MainPageView.as_view(), name="edit_main_page"),
]
