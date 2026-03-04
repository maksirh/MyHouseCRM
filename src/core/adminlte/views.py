from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from src.core.adminlte.forms import (
    AboutUsPageForm,
    ContactsPage,
    ContactsPageForm,
    GalleryFormSet,
    InfoItemsFormset,
    MainPageForm,
    SeoBlockForm,
    ServicePageForm,
)
from src.website.models import AboutUsPage, MainPage, ServicePage


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

        contact = ContactsPage.load()

        if self.request.method == "POST":
            context["contact_form"] = ContactsPageForm(
                self.request.POST, instance=contact
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


class AboutUsPageView(UpdateView):
    model = AboutUsPage
    form_class = AboutUsPageForm
    template_name = "adminlte/about_us_page_edit.html"
    success_url = reverse_lazy("adminlte:edit_about_us_page")

    def get_object(self, **kwargs):
        obj, created = AboutUsPage.objects.get_or_create(id=1)
        return obj

    def get_context_data(self, **kwargs):
        context = super(AboutUsPageView, self).get_context_data(**kwargs)
        about_page = self.get_object()

        if self.request.method == "POST":
            context["main_gallery_formset"] = GalleryFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=about_page.gallery.all(),
                prefix="main_gallery",
            )

            context["add_gallery_formset"] = GalleryFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=about_page.additional_gallery.all(),
                prefix="add_gallery",
            )

            context["seo_block"] = SeoBlockForm(
                self.request.POST, instance=about_page.seo_block
            )

        else:
            context["main_gallery_formset"] = GalleryFormSet(
                queryset=about_page.gallery.all(), prefix="main_gallery"
            )

            context["add_gallery_formset"] = GalleryFormSet(
                queryset=about_page.additional_gallery.all(), prefix="add_gallery"
            )

            context["seo_block"] = SeoBlockForm(instance=about_page.seo_block)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        context = self.get_context_data()

        main_gallery_formset = context["main_gallery_formset"]
        add_gallery_formset = context["add_gallery_formset"]
        seo_form = context["seo_block"]

        if (
            form.is_valid()
            and main_gallery_formset.is_valid()
            and add_gallery_formset.is_valid()
            and seo_form.is_valid()
        ):

            seo_block = seo_form.save()
            about_page = form.save(commit=False)
            about_page.seo_block = seo_block
            about_page.save()

            main_images = main_gallery_formset.save()
            for img in main_images:
                about_page.gallery.add(img)

            add_images = add_gallery_formset.save()
            for img in add_images:
                about_page.additional_gallery.add(img)

            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ServicePageView(UpdateView):
    model = ServicePage
    form_class = ServicePageForm
    template_name = "adminlte/services_page_edit.html"
    success_url = reverse_lazy("adminlte:edit_service_page")

    def get_object(self, **kwargs):
        obj, created = ServicePage.objects.get_or_create(id=1)
        return obj

    def get_context_data(self, **kwargs):
        context = super(ServicePageView, self).get_context_data(**kwargs)
        service_page = self.get_object()

        if self.request.method == "POST":
            context["info"] = InfoItemsFormset(
                self.request.POST,
                self.request.FILES,
                prefix="info",
                queryset=service_page.service.all(),
            )

            context["seo_block"] = SeoBlockForm(
                self.request.POST, instance=service_page.seo_block
            )

        else:
            context["info"] = InfoItemsFormset(
                prefix="info", queryset=service_page.service.all()
            )
            context["seo_block"] = SeoBlockForm(instance=service_page.seo_block)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        context = self.get_context_data()

        services_formset = context["info"]
        seo_form = context["seo_block"]

        if form.is_valid() and services_formset.is_valid() and seo_form.is_valid():
            services_page = form.save(commit=False)
            seo_block = seo_form.save()
            services_page.seo_block = seo_block
            services_page.save()

            saved_services = services_formset.save()
            for service in saved_services:
                services_page.service.add(service)

            return redirect(self.success_url)

        else:
            return self.render_to_response(self.get_context_data(form=form))


class ContactPageView(UpdateView):
    model = ContactsPage
    form_class = ContactsPageForm
    template_name = "adminlte/contacts_page_edit.html"
    success_url = reverse_lazy("adminlte:contacts_edit")

    def get_object(self, queryset=None):
        return ContactsPage.load()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contact = self.object

        if self.request.method == "POST":
            context["seo_block"] = SeoBlockForm(
                self.request.POST, instance=contact.seo_block
            )
        else:
            context["seo_block"] = SeoBlockForm(instance=contact.seo_block)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        context = self.get_context_data()
        seo_form = context["seo_block"]

        if form.is_valid() and seo_form.is_valid():
            seo_instance = seo_form.save()

            contact_instance = form.save(commit=False)
            contact_instance.seo_block = seo_instance
            contact_instance.save()

            return redirect(self.success_url)

        else:
            return self.render_to_response(self.get_context_data(form=form))
