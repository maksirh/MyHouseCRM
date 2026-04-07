import datetime
import json

from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView

from src.crm.models import Receipt, ReceiptItem
from src.house.models import Apartment

from .mixins import CabinetLoginRequiredMixin


class CabinetSummaryView(CabinetLoginRequiredMixin, TemplateView):
    template_name = "crm/summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        flat_id = self.request.GET.get("flat_id")
        if flat_id:
            active_flat = Apartment.objects.filter(owner=user, id=flat_id).first()
        else:
            active_flat = Apartment.objects.filter(owner=user).first()

        context["active_flat"] = active_flat

        if not active_flat:
            return context

        account = active_flat.account
        context["balance"] = account.balance if account else 0.00
        context["account_number"] = account.number if account else "Немає рахунку"

        receipts = Receipt.objects.filter(apartment=active_flat)
        total_spent = receipts.aggregate(total=Sum("total_sum"))["total"] or 0

        months_count = receipts.dates("date", "month").count() or 1
        context["avg_expense"] = float(total_spent) / months_count

        now = timezone.now()
        current_year = now.year
        prev_month_date = now.replace(day=1) - datetime.timedelta(days=1)

        prev_month_items = (
            ReceiptItem.objects.filter(
                receipt__apartment=active_flat,
                receipt__date__year=prev_month_date.year,
                receipt__date__month=prev_month_date.month,
            )
            .values("service__name")
            .annotate(total=Sum("total_price"))
        )

        pie_prev_labels = [item["service__name"] for item in prev_month_items]
        pie_prev_data = [float(item["total"]) for item in prev_month_items]

        curr_year_items = (
            ReceiptItem.objects.filter(
                receipt__apartment=active_flat, receipt__date__year=current_year
            )
            .values("service__name")
            .annotate(total=Sum("total_price"))
        )

        pie_year_labels = [item["service__name"] for item in curr_year_items]
        pie_year_data = [float(item["total"]) for item in curr_year_items]

        monthly_expenses = (
            receipts.filter(date__year=current_year)
            .annotate(month=ExtractMonth("date"))
            .values("month")
            .annotate(total=Sum("total_sum"))
        )

        bar_data = [0] * 12
        for item in monthly_expenses:
            month_idx = item["month"] - 1
            bar_data[month_idx] = float(item["total"])

        context["pie_prev_labels"] = json.dumps(pie_prev_labels)
        context["pie_prev_data"] = json.dumps(pie_prev_data)

        context["pie_year_labels"] = json.dumps(pie_year_labels)
        context["pie_year_data"] = json.dumps(pie_year_data)

        context["bar_data"] = json.dumps(bar_data)

        return context


class CabinetReceiptListView(CabinetLoginRequiredMixin, ListView):
    model = Receipt
    template_name = "crm/receipt_list.html"
    context_object_name = "receipts"
    paginate_by = 15

    def get_queryset(self):
        qs = Receipt.objects.filter(apartment__owner=self.request.user).select_related(
            "apartment__house"
        )

        flat_id = self.request.GET.get("flat_id")
        if flat_id:
            qs = qs.filter(apartment_id=flat_id)

        return qs.order_by("-date", "-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_flat_id"] = self.request.GET.get("flat_id")
        return context


class CabinetReceiptDetailView(CabinetLoginRequiredMixin, DetailView):
    model = Receipt
    template_name = "crm/receipt_detail.html"
    context_object_name = "receipt"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(apartment__owner=self.request.user)
            .select_related(
                "apartment__house", "apartment__section", "tariff", "apartment__account"
            )
            .prefetch_related("items__service", "items__service__measure")
        )


class CabinetTariffView(CabinetLoginRequiredMixin, TemplateView):
    template_name = "crm/tariffs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        flat_id = self.request.GET.get("flat_id")
        if flat_id:
            active_flat = (
                Apartment.objects.filter(owner=user, id=flat_id)
                .select_related("tariff")
                .first()
            )
        else:
            active_flat = (
                Apartment.objects.filter(owner=user).select_related("tariff").first()
            )

        context["active_flat"] = active_flat

        if active_flat and active_flat.tariff:

            context["tariff_services"] = (
                active_flat.tariff.tariffservice_set.select_related(
                    "service", "service__measure", "service__currency"
                ).all()
            )

        return context
