from django.urls import path

from src.crm.views import (
    CabinetCallCreateView,
    CabinetCallListView,
    CabinetMessageDetailView,
    CabinetMessageListView,
    CabinetProfileUpdateView,
    CabinetProfileView,
    CabinetReceiptDetailView,
    CabinetReceiptListView,
    CabinetSummaryView,
    CabinetTariffView,
)

app_name = "src.crm"

urlpatterns = [
    path("summary/", CabinetSummaryView.as_view(), name="summary"),
    path("invoices/", CabinetReceiptListView.as_view(), name="cabinet_invoices"),
    path(
        "invoices/<int:pk>/",
        CabinetReceiptDetailView.as_view(),
        name="cabinet_receipt_detail",
    ),
    path("tariffs/", CabinetTariffView.as_view(), name="cabinet_tariffs"),
    path("messages/", CabinetMessageListView.as_view(), name="cabinet_messages"),
    path(
        "messages/<int:pk>/",
        CabinetMessageDetailView.as_view(),
        name="cabinet_message_detail",
    ),
    path("calls/", CabinetCallListView.as_view(), name="cabinet_calls"),
    path("calls/create/", CabinetCallCreateView.as_view(), name="cabinet_call_create"),
    path("profile/", CabinetProfileView.as_view(), name="cabinet_profile"),
    path(
        "profile/edit/",
        CabinetProfileUpdateView.as_view(),
        name="cabinet_profile_update",
    ),
]
