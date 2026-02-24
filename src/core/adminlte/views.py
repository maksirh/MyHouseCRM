from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from src.core.adminlte.forms import (
    ContactsPageForm,
    InfoItemsFormset,
    MainPageForm,
    SeoBlockForm,
)
from src.website.models import MainPage


class StatisticPageView(TemplateView):
    template_name = "adminlte/statistics.html"

    def get_context_data(self, **kwargs):
        context = super(StatisticPageView, self).get_context_data(**kwargs)
        return context


class MainPageView(UpdateView):
    model = MainPage
    form_class = MainPageForm
    template_name = "adminlte/main_page_edit.html"
    success_url = reverse_lazy("adminlte:edit_main_page")

    def get_object(self, queryset=None):
        obj, created = MainPage.objects.get_or_create(id=1)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_page = self.get_object()

        if self.request.method == "POST":
            context["contact_form"] = ContactsPageForm(
                self.request.POST, instance=main_page.contact
            )
            context["seo_block"] = SeoBlockForm(
                self.request.POST, instance=main_page.seo_block
            )
            context["info_formset"] = InfoItemsFormset(
                self.request.POST,
                self.request.FILES,
                queryset=main_page.info_card.all(),
            )
        else:
            context["contact_form"] = ContactsPageForm(instance=main_page.contact)
            context["seo_block"] = SeoBlockForm(instance=main_page.seo_block)
            context["info_formset"] = InfoItemsFormset(
                queryset=main_page.info_card.all()
            )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        context = self.get_context_data()

        contact_form = context["contact_form"]
        seo_form = context["seo_block"]
        info_formset = context["info_formset"]

        main_valid = form.is_valid()
        contact_valid = contact_form.is_valid()
        seo_valid = seo_form.is_valid()
        info_valid = info_formset.is_valid()

        if main_valid and contact_valid and seo_valid and info_valid:
            contact = contact_form.save()
            seo_block = seo_form.save()

            main_page = form.save(commit=False)
            main_page.contact = contact
            main_page.seo_block = seo_block
            main_page.save()

            info_items = info_formset.save()

            for item in info_items:
                main_page.info_card.add(item)

            return redirect(self.success_url)

        else:

            return self.render_to_response(self.get_context_data(form=form))
