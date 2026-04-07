from django.urls import path

from src.crm.views import (
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
]
