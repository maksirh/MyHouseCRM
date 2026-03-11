from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
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
    ArticleForm,
    ContactsPage,
    ContactsPageForm,
    FloorFormSet,
    GalleryFormSet,
    HouseForm,
    HouseUserFormSet,
    InfoItemsFormset,
    MainPageForm,
    MeasureFormSet,
    PaymentDetail,
    PaymentDetailForm,
    SectionFormSet,
    SeoBlockForm,
    ServiceFormSet,
    ServicePageForm,
    TariffServiceFormSet,
    TariffsForm,
    UserForm,
    UserProfileForm,
)
from src.crm.models import Article, Measure, Service, Tariffs
from src.house.models import House
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


def tariff_update(request, pk=None):
    if pk:
        tariff = get_object_or_404(Tariffs, pk=pk)
    else:
        tariff = Tariffs()

    if request.method == "POST":
        form = TariffsForm(request.POST, instance=tariff)
        formset = TariffServiceFormSet(request.POST, instance=tariff)

        if form.is_valid() and formset.is_valid():
            saved_tariff = form.save()
            formset.instance = saved_tariff
            formset.save()
            return redirect("adminlte:tariff_list")
    else:
        form = TariffsForm(instance=tariff)
        formset = TariffServiceFormSet(instance=tariff)

    return render(
        request,
        "adminlte/tariff_edit.html",
        {
            "tariff": tariff,
            "form": form,
            "formset": formset,
        },
    )


def get_service_unit(request):
    service_id = request.GET.get("service_id")
    if service_id:
        service = Service.objects.filter(id=service_id).first()
        if service:
            return JsonResponse(
                {
                    "unit_name": service.measure.name if service.measure else "",
                    "currency": service.currency.name if service.currency else "грн",
                }
            )
    return JsonResponse({"unit_name": "", "currency": ""})


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


def get_user_role(request):
    user_id = request.GET.get("user_id")
    if user_id:
        try:
            user = User.objects.select_related("role").get(pk=user_id)
            role_name = user.role.name if user.role else "Без ролі"

            return JsonResponse({"role_name": role_name})
        except User.DoesNotExist:
            pass

    return JsonResponse({"role_name": "Помилка"}, status=400)


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
