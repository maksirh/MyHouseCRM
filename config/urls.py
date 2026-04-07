from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from src.core.adminlte.api import api as admin_api
from src.crm.api import api as crm_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("src.website.urls", namespace="website")),
    path("adminpanel/", include("src.core.adminlte.urls", namespace="adminlte")),
    path("auth/", include("src.authentication.urls", namespace="authentication")),
    path("cabinet/", include("src.crm.urls", namespace="crm")),
    path("cabinet/api/", crm_api.urls),
    path("adminpanel/api/", admin_api.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
