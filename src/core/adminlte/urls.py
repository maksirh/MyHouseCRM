from django.urls import path

from .views import AboutUsPageView, MainPageView, ServicePageView, StatisticPageView

app_name = "adminlte"

urlpatterns = [
    path("", StatisticPageView.as_view(), name="statistic"),
    path("managesite/mainpage", MainPageView.as_view(), name="edit_main_page"),
    path("managesite/aboutus", AboutUsPageView.as_view(), name="edit_about_us_page"),
    path("managesite/services", ServicePageView.as_view(), name="edit_service_page"),
]
