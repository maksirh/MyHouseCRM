import json

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Case, Count, Q, Sum, When
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from src.core.adminlte.forms import (
    AboutUsPageForm,
    ApartmentForm,
    ArticleForm,
    CashBoxExpenseForm,
    CashBoxIncomeForm,
    ContactsPage,
    ContactsPageForm,
    CounterReadingForm,
    FloorFormSet,
    GalleryFormSet,
    HouseForm,
    HouseUserFormSet,
    InfoItemsFormset,
    MainPageForm,
    MeasureFormSet,
    PaymentDetail,
    PaymentDetailForm,
    PersonalAccountForm,
    ReceiptForm,
    ReceiptItemFormSet,
    SectionFormSet,
    SeoBlockForm,
    ServiceFormSet,
    ServicePageForm,
    TariffServiceFormSet,
    TariffsForm,
    UserForm,
    UserProfileForm,
)
from src.crm.models import (
    Article,
    CashBox,
    CounterReadings,
    Measure,
    PersonalAccount,
    Receipt,
    Service,
    Tariffs,
)
from src.house.models import Apartment, Floor, House, Section
from src.user.models import Roles, User
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


class RolesUpdateView(View):
    PERMISSIONS = [
        "has_statistics",
        "has_cashbox",
        "has_receipt",
        "has_own_account",
        "has_apartment",
        "has_owner_apartments",
        "has_message",
        "has_call_master",
        "has_counter",
        "has_manage_site",
        "has_service",
        "has_tariffs",
        "has_roles",
        "has_user",
        "has_account_detail",
    ]

    def get(self, request):
        roles = Roles.objects.all()
        return render(request, "adminlte/roles.html", {"roles": roles})

    def post(self, request):
        roles = Roles.objects.all()

        for role in roles:
            for perm in self.PERMISSIONS:
                checkbox_name = f"{perm}_{role.id}"

                is_checked = checkbox_name in request.POST
                setattr(role, perm, is_checked)

            role.save()

        return redirect("adminlte:roles_update")


class UserEditView(UpdateView):
    model = User
    form_class = UserForm
    template_name = "adminlte/edit_user.html"
    success_url = reverse_lazy("adminlte:users_list")

    def form_valid(self, form):
        form.instance.username = form.cleaned_data.get("email")

        raw_password = form.cleaned_data.get("password")
        if raw_password:
            form.instance.set_password(raw_password)

        phone = form.cleaned_data.get("phone")
        if phone:
            form.instance.phone_number = phone

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = Roles.objects.all()
        return context


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = "adminlte/edit_user.html"
    success_url = reverse_lazy("adminlte:users_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = Roles.objects.all()
        return context

    def form_valid(self, form):
        form.instance.username = form.cleaned_data.get("email")

        raw_password = form.cleaned_data.get("password")
        if raw_password:
            form.instance.set_password(raw_password)

        phone = form.cleaned_data.get("phone")
        if phone:
            form.instance.phone_number = phone

        return super().form_valid(form)


class UserListView(ListView):
    model = User
    template_name = "adminlte/users_list.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.all()

        name_query = self.request.GET.get("name")
        if name_query:
            queryset = queryset.filter(
                Q(first_name__icontains=name_query) | Q(last_name__icontains=name_query)
            )

        role_query = self.request.GET.get("role")
        if role_query:
            queryset = queryset.filter(role__name__iexact=role_query)

        phone_query = self.request.GET.get("phone")
        if phone_query:
            queryset = queryset.filter(phone_number__icontains=phone_query)

        email_query = self.request.GET.get("email")
        if email_query:
            queryset = queryset.filter(email__icontains=email_query)

        status_query = self.request.GET.get("status")
        if status_query:
            queryset = queryset.filter(status=status_query)

        sort_by = self.request.GET.get("sort")
        if sort_by == "name":
            queryset = queryset.order_by("first_name", "last_name")
        elif sort_by == "-name":
            queryset = queryset.order_by("-first_name", "-last_name")
        elif sort_by == "role":
            queryset = queryset.order_by("role__name")
        else:
            queryset = queryset.order_by("-id")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = Roles.objects.all()
        context["query_params"] = self.request.GET.urlencode()
        return context


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "adminlte/user_profile.html"
    success_url = reverse_lazy("adminlte:user_profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Ваш профіль успішно оновлено!")
        return super().form_valid(form)


class UserDetailView(DetailView):
    model = User
    template_name = "adminlte/user_detail.html"
    context_object_name = "target_user"


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy("adminlte:users_list")


class ServiceEditView(View):
    template_name = "adminlte/service_edit.html"

    def get(self, request):
        service_formset = ServiceFormSet(
            queryset=Service.objects.all(), prefix="service"
        )
        measure_formset = MeasureFormSet(
            queryset=Measure.objects.all(), prefix="measure"
        )

        context = {
            "service_formset": service_formset,
            "measure_formset": measure_formset,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        service_formset = ServiceFormSet(request.POST, prefix="service")
        measure_formset = MeasureFormSet(request.POST, prefix="measure")

        if service_formset.is_valid() and measure_formset.is_valid():
            service_formset.save()
            measure_formset.save()

            return redirect("adminlte:service_edit")
        else:
            print("ПОМИЛКИ ФОРМИ ПОСЛУГИ:", service_formset.errors)
        context = {
            "service_formset": service_formset,
            "measure_formset": measure_formset,
        }

        return render(request, self.template_name, context)


class TariffListView(ListView):
    model = Tariffs
    template_name = "adminlte/tariffs.html"
    context_object_name = "tariffs"

    def get_queryset(self):
        qs = super().get_queryset()

        sort_by = self.request.GET.get("sort")

        allowed_sort_fields = ["name", "-name", "updated_at", "-updated_at"]

        if sort_by in allowed_sort_fields:
            qs = qs.order_by(sort_by)
        else:
            qs = qs.order_by("-updated_at")

        return qs


class TariffDetailView(DetailView):
    model = Tariffs
    template_name = "adminlte/tariff_info.html"
    context_object_name = "tariff"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tariff_services"] = self.object.tariffservice_set.select_related(
            "service", "service__measure", "service__currency"
        ).all()

        return context


class PaymentDetailView(UpdateView):
    model = PaymentDetail
    form_class = PaymentDetailForm
    template_name = "adminlte/payment_details.html"
    success_url = reverse_lazy("adminlte:payment_detail")

    def get_object(self, queryset=None):
        obj, created = PaymentDetail.objects.get_or_create(id=1)
        return obj


class ListArticleView(ListView):
    model = Article
    template_name = "adminlte/payments_articles.html"
    context_object_name = "articles"


class CreateArticleView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "adminlte/payment_article_edit.html"
    success_url = reverse_lazy("adminlte:article_list")


class EditArticleView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "adminlte/payment_article_edit.html"
    success_url = reverse_lazy("adminlte:article_list")


class DeleteArticleView(DeleteView):
    model = Article
    success_url = reverse_lazy("adminlte:article_list")


class HouseView(View):
    template_name = "adminlte/edit_house.html"

    def get_object(self, pk):
        if pk:
            return get_object_or_404(House, pk=pk)
        return House()

    def get(self, request, pk=None):
        house = self.get_object(pk)

        form = HouseForm(instance=house)
        section_formset = SectionFormSet(instance=house, prefix="sections")
        floor_formset = FloorFormSet(instance=house, prefix="floors")
        user_formset = HouseUserFormSet(instance=house, prefix="users")

        context = {
            "house": house,
            "form": form,
            "section_formset": section_formset,
            "floor_formset": floor_formset,
            "user_formset": user_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        house = self.get_object(pk)

        form = HouseForm(request.POST, request.FILES, instance=house)
        section_formset = SectionFormSet(
            request.POST, instance=house, prefix="sections"
        )
        floor_formset = FloorFormSet(request.POST, instance=house, prefix="floors")
        user_formset = HouseUserFormSet(request.POST, instance=house, prefix="users")

        if (
            form.is_valid()
            and section_formset.is_valid()
            and floor_formset.is_valid()
            and user_formset.is_valid()
        ):
            saved_house = form.save()

            section_formset.instance = saved_house
            section_formset.save()

            floor_formset.instance = saved_house
            floor_formset.save()

            user_formset.instance = saved_house
            user_formset.save()

            return redirect("adminlte:house_list")

        context = {
            "house": house,
            "form": form,
            "section_formset": section_formset,
            "floor_formset": floor_formset,
            "user_formset": user_formset,
        }
        return render(request, self.template_name, context)


class HouseListView(ListView):
    model = House
    template_name = "adminlte/house_list.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()

        name = self.request.GET.get("name")
        address = self.request.GET.get("address")
        sort_by = self.request.GET.get("sort")

        if name:
            qs = qs.filter(name__icontains=name)
        if address:
            qs = qs.filter(address__icontains=address)

        allowed_sort_fields = ["name", "-name", "address", "-address"]
        if sort_by in allowed_sort_fields:
            qs = qs.order_by(sort_by)
        else:
            qs = qs.order_by("-id")

        return qs


class HouseDetailView(DetailView):
    model = House
    template_name = "adminlte/house_info.html"
    context_object_name = "house"

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.prefetch_related("users")


class HouseDeleteView(DeleteView):
    model = House
    success_url = reverse_lazy("adminlte:house_list")


class ApartmentCreateView(CreateView):
    model = Apartment
    template_name = "adminlte/apartment_edit.html"
    form_class = ApartmentForm
    success_url = reverse_lazy("adminlte:apartment_list")


class ApartmentUpdateView(UpdateView):
    model = Apartment
    template_name = "adminlte/apartment_edit.html"
    form_class = ApartmentForm
    success_url = reverse_lazy("adminlte:apartment_list")


class ApartmentDeleteView(DeleteView):
    model = Apartment
    success_url = reverse_lazy("adminlte:apartment_list")


class ApartmentListView(ListView):
    model = Apartment
    template_name = "adminlte/apartment_list.html"
    paginate_by = 10
    context_object_name = "flats"

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("house", "section", "floor", "owner", "account")
        )

        number = self.request.GET.get("number")
        house_id = self.request.GET.get("house_id")
        section_id = self.request.GET.get("section_id")
        floor_id = self.request.GET.get("floor_id")
        user_id = self.request.GET.get("user_id")
        has_debt = self.request.GET.get("has_debt")
        sort = self.request.GET.get("sort")

        if number:
            qs = qs.filter(number__icontains=number)
        if house_id:
            qs = qs.filter(house_id=house_id)
        if section_id:
            qs = qs.filter(section_id=section_id)
        if floor_id:
            qs = qs.filter(floor_id=floor_id)
        if user_id:
            qs = qs.filter(owner_id=user_id)

        if has_debt == "1":
            qs = qs.filter(account__balance__lt=0)
        elif has_debt == "0":
            qs = qs.filter(account__balance__gte=0)

        allowed_sorts = {
            "number": "number",
            "-number": "-number",
            "house": "house__name",
            "-house": "-house__name",
            "section": "section__name",
            "-section": "-section__name",
            "floor": "floor__name",
            "-floor": "-floor__name",
            "owner": "owner__first_name",
            "-owner": "-owner__first_name",
        }

        if sort in allowed_sorts:
            qs = qs.order_by(allowed_sorts[sort])
        else:
            qs = qs.order_by("-id")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()
        context["owners"] = User.objects.filter(apartment__isnull=False).distinct()

        house_id = self.request.GET.get("house_id")
        if house_id:
            context["filter_sections"] = Section.objects.filter(house_id=house_id)
            context["filter_floors"] = Floor.objects.filter(house_id=house_id)

        return context


class ApartmentDetailView(DetailView):
    model = Apartment
    template_name = "adminlte/apartment.html"
    context_object_name = "flat"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("house", "section", "floor", "owner", "tariff", "account")
        )


class OwnerListView(ListView):
    model = User
    template_name = "adminlte/apartment_owners.html"
    context_object_name = "owners"
    paginate_by = 10

    def get_queryset(self):
        qs = User.objects.prefetch_related("apartment_set__house").annotate(
            debt_flats=Count(Case(When(apartment__account__balance__lt=0, then=1)))
        )

        uid = self.request.GET.get("uid")
        fullname = self.request.GET.get("fullname")
        phone = self.request.GET.get("phone")
        email = self.request.GET.get("email")
        house_id = self.request.GET.get("house")
        flat_number = self.request.GET.get("flat")
        status = self.request.GET.get("status")
        has_debt = self.request.GET.get("has_debt")
        sort = self.request.GET.get("sort")

        if uid:
            qs = qs.filter(id__icontains=uid)
        if fullname:
            qs = qs.filter(
                Q(first_name__icontains=fullname)
                | Q(last_name__icontains=fullname)
                | Q(surname__icontains=fullname)
            )
        if phone:
            qs = qs.filter(phone_number__icontains=phone)
        if email:
            qs = qs.filter(email__icontains=email)
        if house_id:
            qs = qs.filter(apartment__house_id=house_id)
        if flat_number:
            qs = qs.filter(apartment__number__icontains=flat_number)
        if status:
            qs = qs.filter(status=status)

        if has_debt == "1":
            qs = qs.filter(debt_flats__gt=0)

        qs = qs.distinct()

        if sort == "fullname":
            qs = qs.order_by("first_name", "last_name")
        elif sort == "-fullname":
            qs = qs.order_by("-first_name", "-last_name")
        elif sort == "created":
            qs = qs.order_by("date_joined")
        elif sort == "-created":
            qs = qs.order_by("-date_joined")
        else:
            qs = qs.order_by("-id")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["houses"] = House.objects.all()
        return context


class AccountCreateView(CreateView):
    model = PersonalAccount
    form_class = PersonalAccountForm
    template_name = "adminlte/account_edit.html"
    success_url = reverse_lazy("adminlte:account_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        apartment = form.cleaned_data.get("apartment")

        if apartment:
            apartment.account = self.object
            apartment.save()

        return response


class AccountListView(ListView):
    model = PersonalAccount
    template_name = "adminlte/account_list.html"
    context_object_name = "accounts"
    paginate_by = 10

    def get_queryset(self):
        qs = PersonalAccount.objects.prefetch_related(
            "apartment_set__house", "apartment_set__section", "apartment_set__owner"
        )

        number = self.request.GET.get("number")
        status = self.request.GET.get("status")
        apartment = self.request.GET.get("apartment")
        house_id = self.request.GET.get("house")
        section_id = self.request.GET.get("section")
        owner_id = self.request.GET.get("owner")
        has_debt = self.request.GET.get("has_debt")
        sort = self.request.GET.get("sort")

        if number:
            qs = qs.filter(number__icontains=number)
        if status in ["True", "False"]:
            qs = qs.filter(status=(status == "True"))
        if apartment:
            qs = qs.filter(apartment__number__icontains=apartment)
        if house_id:
            qs = qs.filter(apartment__house_id=house_id)
        if section_id:
            qs = qs.filter(apartment__section_id=section_id)
        if owner_id:
            qs = qs.filter(apartment__owner_id=owner_id)

        if has_debt == "1":
            qs = qs.filter(balance__lt=0)
        elif has_debt == "0":
            qs = qs.filter(balance__gte=0)

        if sort == "number":
            qs = qs.order_by("number")
        elif sort == "-number":
            qs = qs.order_by("-number")
        elif sort == "balance":
            qs = qs.order_by("balance")
        elif sort == "-balance":
            qs = qs.order_by("-balance")
        else:
            qs = qs.order_by("-id")

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["houses"] = House.objects.all()
        context["owners"] = User.objects.filter(apartment__isnull=False).distinct()

        house_id = self.request.GET.get("house")
        if house_id:
            context["filter_sections"] = Section.objects.filter(house_id=house_id)

        balance_agg = PersonalAccount.objects.filter(balance__gt=0).aggregate(
            total=Sum("balance")
        )
        context["accounts_balance"] = balance_agg["total"] or 0.00

        debt_agg = PersonalAccount.objects.filter(balance__lt=0).aggregate(
            total=Sum("balance")
        )
        context["accounts_debt"] = abs(debt_agg["total"]) if debt_agg["total"] else 0.00

        context["cashbox_state"] = float(context["accounts_balance"]) - float(
            context["accounts_debt"]
        )

        return context


class AccountDetailView(DetailView):
    model = PersonalAccount
    template_name = "adminlte/account_detail.html"
    context_object_name = "account"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "apartment_set__house", "apartment_set__section", "apartment_set__owner"
            )
        )


class AccountUpdateView(UpdateView):
    model = PersonalAccount
    form_class = PersonalAccountForm
    template_name = "adminlte/account_edit.html"
    success_url = reverse_lazy("adminlte:account_list")

    def get_initial(self):
        initial = super().get_initial()
        flat = self.object.apartment_set.first()

        if flat:
            initial["apartment"] = flat.id
            if flat.section:
                initial["section"] = flat.section.id
            if flat.house:
                initial["house"] = flat.house.id

        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        new_apartment = form.cleaned_data.get("apartment")

        self.object.apartment_set.update(account=None)

        if new_apartment:
            new_apartment.account = self.object
            new_apartment.save()

        return response


class AccountDeleteView(DeleteView):
    model = PersonalAccount
    success_url = reverse_lazy("adminlte:account_list")


class CounterReadingCreateView(CreateView):
    model = CounterReadings
    form_class = CounterReadingForm
    template_name = "adminlte/counter_reading_edit.html"
    success_url = reverse_lazy("adminlte:counter_reading")

    def form_valid(self, form):
        response = super().form_valid(form)
        if "save_and_add" in self.request.POST:
            return HttpResponseRedirect(reverse_lazy("adminlte:counter_reading_create"))
        return response


class CounterReadingHistoryView(ListView):
    model = CounterReadings
    template_name = "adminlte/counter_history.html"
    context_object_name = "counter_history"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("apartment__house", "apartment__section", "service")
        )

        flat_id = self.request.GET.get("flat_id")
        service_id = self.request.GET.get("service_id")
        number = self.request.GET.get("number")
        status = self.request.GET.get("status")
        date_filter = self.request.GET.get("date")
        house = self.request.GET.get("house")
        section = self.request.GET.get("section")
        flat_number = self.request.GET.get("flat_number")
        service = self.request.GET.get("service")
        sort = self.request.GET.get("sort")

        if flat_id:
            qs = qs.filter(apartment_id=flat_id)
        if service_id:
            qs = qs.filter(service_id=service_id)
        if number:
            qs = qs.filter(number__icontains=number)
        if status:
            qs = qs.filter(status=status)
        if date_filter:
            qs = qs.filter(date__icontains=date_filter)
        if house:
            qs = qs.filter(apartment__house_id=house)
        if section:
            qs = qs.filter(apartment__section_id=section)
        if flat_number:
            qs = qs.filter(apartment__number__icontains=flat_number)
        if service:
            qs = qs.filter(service_id=service)

        if sort == "-date":
            qs = qs.order_by("-date")
        elif sort == "date":
            qs = qs.order_by("date")
        elif sort == "-month":
            qs = qs.order_by("-date")
        elif sort == "month":
            qs = qs.order_by("date")
        else:
            qs = qs.order_by("-id")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        flat_id = self.request.GET.get("flat_id")
        service_id = self.request.GET.get("service_id")

        if flat_id:
            context["flat"] = get_object_or_404(Apartment, id=flat_id)
        if service_id:
            context["service"] = get_object_or_404(Service, id=service_id)

        context["houses"] = House.objects.all()
        context["services"] = Service.objects.all()

        house_id = self.request.GET.get("house")
        if house_id:
            context["filter_sections"] = Section.objects.filter(house_id=house_id)

        return context


class CounterReadingUpdateView(UpdateView):
    model = CounterReadings
    form_class = CounterReadingForm
    template_name = "adminlte/counter_reading_edit.html"
    success_url = reverse_lazy("adminlte:counter_reading_history")

    def get_initial(self):
        initial = super().get_initial()
        if self.object and self.object.apartment:
            apartment = self.object.apartment
            initial["apartment"] = apartment.id
            if apartment.house:
                initial["house"] = apartment.house.id
            if apartment.section:
                initial["section"] = apartment.section.id
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        if "save_and_add" in self.request.POST:
            return HttpResponseRedirect(reverse_lazy("adminlte:counter_reading_create"))
        return response


class CounterReadingDetailView(DetailView):
    model = CounterReadings
    template_name = "adminlte/counter_reading_detail.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "apartment__house", "apartment__section", "apartment__owner", "service"
            )
        )


def get_lists_by_house(request):
    house_id = request.GET.get("house_id")
    section_id = request.GET.get("section_id")

    sections_html = '<option value="">Оберіть...</option>'
    flats_html = '<option value="">Оберіть...</option>'

    if house_id:
        sections = Section.objects.filter(house_id=house_id)
        for section in sections:
            sections_html += f'<option value="{section.id}">{section.name}</option>'

        flats = Apartment.objects.filter(house_id=house_id)

        if section_id:
            flats = flats.filter(section_id=section_id)

        for flat in flats:
            flats_html += f'<option value="{flat.id}">{flat.number}</option>'

    return JsonResponse({"sections": sections_html, "flats": flats_html})


class CounterReadingDeleteView(DeleteView):
    model = CounterReadings
    success_url = reverse_lazy("adminlte:counter_reading_history")


class ReceiptListView(ListView):
    model = Receipt
    template_name = "adminlte/receipt_list.html"
    context_object_name = "receipts"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("apartment__owner", "apartment__house")
        )

        number = self.request.GET.get("number")
        status = self.request.GET.get("status")
        date_filter = self.request.GET.get("date")
        period = self.request.GET.get("period")
        apartment_number = self.request.GET.get("apartment")
        owner_id = self.request.GET.get("owner")
        is_made_payment = self.request.GET.get("is_made_payment")

        if number:
            qs = qs.filter(number__icontains=number)
        if status:
            qs = qs.filter(status=status)
        if date_filter:
            qs = qs.filter(date__icontains=date_filter)
        if period:
            qs = qs.filter(period__icontains=period)
        if apartment_number:
            qs = qs.filter(apartment__number__icontains=apartment_number)
        if owner_id:
            qs = qs.filter(apartment__owner_id=owner_id)
        if is_made_payment:
            is_made = True if is_made_payment == "1" else False
            qs = qs.filter(is_made_payment=is_made)

        qs = qs.order_by("-date", "-id")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        balance_agg = PersonalAccount.objects.filter(balance__gt=0).aggregate(
            total=Sum("balance")
        )
        context["accounts_balance"] = balance_agg["total"] or 0.00

        debt_agg = PersonalAccount.objects.filter(balance__lt=0).aggregate(
            total=Sum("balance")
        )
        context["accounts_debt"] = abs(debt_agg["total"]) if debt_agg["total"] else 0.00

        context["cashbox_state"] = float(context["accounts_balance"]) - float(
            context["accounts_debt"]
        )

        context["owners"] = User.objects.all()

        return context


class ReceiptDetailView(DetailView):
    model = Receipt
    template_name = "adminlte/receipt_detail.html"
    context_object_name = "receipt"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "apartment__house", "apartment__section", "apartment__owner", "tariff"
            )
            .prefetch_related("items__service")
        )


class ReceiptCreateView(CreateView):
    model = Receipt
    form_class = ReceiptForm
    template_name = "adminlte/receipt_form.html"
    success_url = reverse_lazy("adminlte:receipt_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = ReceiptItemFormSet(self.request.POST)
        else:
            data["formset"] = ReceiptItemFormSet()

        services = Service.objects.select_related("measure").all()
        units_dict = {
            str(s.id): (str(s.measure) if s.measure else "-") for s in services
        }
        data["service_units"] = json.dumps(units_dict)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        with transaction.atomic():
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object

                formset.save()

                receipt_total = sum(
                    item.quantity * item.price_per_unit
                    for item in self.object.items.all()
                )

                self.object.total_sum = receipt_total
                self.object.save()

            else:
                return self.form_invalid(form)

        return super().form_valid(form)


def get_apartment_info(request):
    apartment_id = request.GET.get("apartment_id")
    if apartment_id:
        try:
            apt = Apartment.objects.get(id=apartment_id)
            owner_name = (
                f"{apt.owner.first_name} {apt.owner.last_name}"
                if apt.owner
                else "Не обрано"
            )

            owner_phone = (
                apt.owner.phone_number
                if apt.owner and getattr(apt.owner, "phone_number", None)
                else "Немає телефону"
            )
            account = PersonalAccount.objects.filter(apartment=apt).first()
            account_number = account.number if account else "Рахунок не створено"
            tariff_id = (
                apt.tariff_id if hasattr(apt, "tariff_id") and apt.tariff_id else ""
            )

            return JsonResponse(
                {
                    "owner_name": owner_name,
                    "owner_phone": owner_phone,
                    "account_number": account_number,
                    "tariff_id": tariff_id,
                }
            )
        except Apartment.DoesNotExist:
            pass

    return JsonResponse({"error": "Not found"}, status=404)


class ReceiptUpdateView(UpdateView):
    model = Receipt
    form_class = ReceiptForm
    template_name = "adminlte/receipt_form.html"
    success_url = reverse_lazy("adminlte:receipt_list")

    def get_initial(self):
        initial = super().get_initial()
        if self.object and self.object.apartment:
            initial["house"] = self.object.apartment.house_id
            if self.object.apartment.section:
                initial["section"] = self.object.apartment.section_id
        return initial

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = ReceiptItemFormSet(
                self.request.POST, instance=self.object
            )
        else:
            data["formset"] = ReceiptItemFormSet(instance=self.object)

        if self.object and self.object.apartment:
            apt = self.object.apartment
            data["owner_name"] = (
                f"{apt.owner.first_name} {apt.owner.last_name}"
                if apt.owner
                else "не обрано"
            )

            data["owner_phone"] = (
                apt.owner.phone_number
                if apt.owner and apt.owner.phone_number
                else "Немає телефону"
            )

            account = PersonalAccount.objects.filter(apartment=apt).first()
            data["account_number"] = (
                account.number if account else "Рахунок не створено"
            )

        else:
            data["owner_name"] = "не обрано"
            data["owner_phone"] = "не обрано"
            data["account_number"] = "не обрано"

        services = Service.objects.select_related("measure").all()
        units_dict = {
            str(s.id): (str(s.measure) if s.measure else "-") for s in services
        }
        data["service_units"] = json.dumps(units_dict)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        with transaction.atomic():
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()

                receipt_total = sum(
                    item.quantity * item.price_per_unit
                    for item in self.object.items.all()
                )

                self.object.total_sum = receipt_total
                self.object.save()

            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class ReceiptDeleteView(DeleteView):
    model = Receipt
    template_name = "adminlte/receipt_confirm_delete.html"
    success_url = reverse_lazy("adminlte:receipt_list")


class TariffCreateView(CreateView):
    model = Tariffs
    form_class = TariffsForm
    template_name = "adminlte/tariff_edit.html"
    success_url = reverse_lazy("adminlte:tariff_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = TariffServiceFormSet(self.request.POST)
        else:
            data["formset"] = TariffServiceFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        with transaction.atomic():
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class TariffUpdateView(UpdateView):
    model = Tariffs
    form_class = TariffsForm
    template_name = "adminlte/tariff_edit.html"
    success_url = reverse_lazy("adminlte:tariff_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = TariffServiceFormSet(
                self.request.POST, instance=self.object
            )
        else:
            data["formset"] = TariffServiceFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        with transaction.atomic():
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


def send_user_invite(request, pk):
    target_user = get_object_or_404(User, pk=pk)

    if not target_user.email:
        messages.error(
            request, "Неможливо надіслати запрошення: у користувача немає Email."
        )
        return redirect("users_list")

    subject = "Запрошення до системи MyHouseCRM"
    message = f"""Вітаємо, {target_user.first_name or 'Користувачу'}!

Вас запрошено до системи управління MyHouseCRM.
Ваш логін для входу: {target_user.email}

Для входу перейдіть за посиланням:

З повагою, Адміністрація."""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[target_user.email],
            fail_silently=False,
        )
        messages.success(
            request, f"Запрошення успішно надіслано на {target_user.email}"
        )
    except Exception as e:
        messages.error(request, f"Помилка при відправці листа: {e}")

    return redirect("adminlte:users_list")


class CashBoxListView(ListView):
    model = CashBox
    template_name = "adminlte/cashbox_list.html"
    context_object_name = "cashbox_list"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("article", "manager", "personal_account")
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        balance_agg = PersonalAccount.objects.filter(balance__gt=0).aggregate(
            total=Sum("balance")
        )
        context["accounts_balance"] = balance_agg["total"] or 0.00

        debt_agg = PersonalAccount.objects.filter(balance__lt=0).aggregate(
            total=Sum("balance")
        )
        context["accounts_debt"] = abs(debt_agg["total"]) if debt_agg["total"] else 0.00

        income = (
            CashBox.objects.filter(is_completed=True, article__article="I").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        expense = (
            CashBox.objects.filter(is_completed=True, article__article="E").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        context["cashbox_state"] = income - expense

        context["total_income"] = income
        context["total_expense"] = expense

        return context


class CashBoxIncomeCreateView(CreateView):
    model = CashBox
    form_class = CashBoxIncomeForm
    template_name = "adminlte/cashbox_income_form.html"
    success_url = reverse_lazy("adminlte:cashbox_list")

    def get_initial(self):
        initial = super().get_initial()
        last_cashbox = CashBox.objects.order_by("id").last()
        next_id = last_cashbox.id + 1 if last_cashbox else 1
        initial["number"] = f"{next_id:010d}"
        return initial


class CashBoxExpenseCreateView(CreateView):
    model = CashBox
    form_class = CashBoxExpenseForm
    template_name = "adminlte/cashbox_expense_form.html"
    success_url = reverse_lazy("adminlte:cashbox_list")

    def get_initial(self):
        initial = super().get_initial()
        last_cashbox = CashBox.objects.order_by("id").last()
        next_id = last_cashbox.id + 1 if last_cashbox else 1
        initial["number"] = f"{next_id:010d}"
        return initial


class CashBoxUpdateView(UpdateView):
    model = CashBox
    success_url = reverse_lazy("adminlte:cashbox_list")

    def get_form_class(self):
        if self.object.article.article == "I":
            return CashBoxIncomeForm
        return CashBoxExpenseForm

    def get_template_names(self):
        if self.object.article.article == "I":
            return ["adminlte/cashbox_income_form.html"]
        return ["adminlte/cashbox_expense_form.html"]


class CashBoxDeleteView(DeleteView):
    model = CashBox
    success_url = reverse_lazy("adminlte:cashbox_list")
