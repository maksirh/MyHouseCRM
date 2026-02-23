from django.urls import path

from .views import AboutUsPageView, HomePageView

app_name = "website"

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("about/", AboutUsPageView.as_view(), name="about_page"),
]
