from django.urls import path

from .views import AboutUsPageView, ContactPageView, HomePageView, ServicePageView

app_name = "website"

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("about/", AboutUsPageView.as_view(), name="about_page"),
    path("services/", ServicePageView.as_view(), name="services_page"),
    path("contacts/", ContactPageView.as_view(), name="contacts_page"),
]
