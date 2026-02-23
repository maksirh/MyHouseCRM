from django.urls import path

from .views import StatisticPageView

app_name = "adminlte"

urlpatterns = [
    path("", StatisticPageView.as_view(), name="statistic"),
]
