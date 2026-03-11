from django import forms
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory

from src.crm.models import (
    Article,
    Measure,
    PaymentDetail,
    Service,
    Tariffs,
    TariffService,
)
from src.house.models import Floor, House, HouseUser, Section
from src.user.models import User
from src.website.models import (
    AboutUsPage,
    ContactsPage,
    Gallery,
    InfoItems,
    MainPage,
    SeoBlock,
    ServicePage,
)


class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock

        fields = ["title", "description", "keywords"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "keywords": forms.Textarea(attrs={"class": "form-control"}),
        }


class ContactsPageForm(forms.ModelForm):
    class Meta:
        model = ContactsPage

        fields = [
            "name",
            "location",
            "title",
            "description",
            "email",
            "phone_number",
            "longitude",
            "latitude",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control"}),
            "latitude": forms.NumberInput(attrs={"class": "form-control"}),
        }


class InfoItemsForm(forms.ModelForm):
    class Meta:
        model = InfoItems

        fields = ["title", "description", "image"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


InfoItemsFormset = modelformset_factory(
    InfoItems, form=InfoItemsForm, extra=0, can_delete=True
)


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage

        fields = ["title", "slide1", "slide2", "slide3"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slide1": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "slide2": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "slide3": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ["image"]


GalleryFormSet = modelformset_factory(
    Gallery, form=GalleryForm, extra=1, can_delete=True
)


class AboutUsPageForm(forms.ModelForm):
    class Meta:
        model = AboutUsPage

        fields = [
            "title",
            "description",
            "director_photo",
            "additional_title",
            "additional_description",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "director_photo": forms.FileInput(attrs={"class": "form-control"}),
            "additional_title": forms.TextInput(attrs={"class": "form-control"}),
            "additional_description": forms.Textarea(attrs={"class": "form-control"}),
        }


class ServicePageForm(forms.ModelForm):
    class Meta:
        model = ServicePage
        fields = []


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False)
    password_confirm = forms.CharField(required=False)

    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "surname",
            "email",
            "role",
            "phone_number",
            "birth_date",
            "viber",
            "telegram",
            "status",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control"}),
            "viber": forms.TextInput(attrs={"class": "form-control"}),
            "telegram": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error(
                "password_confirm", "Паролі не співпадають. Спробуйте ще раз."
            )

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "email"]


class MeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "measure", "currency"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "measure": forms.Select(attrs={"class": "form-control"}),
            "currency": forms.Select(attrs={"class": "form-control"}),
        }


MeasureFormSet = modelformset_factory(
    Measure, form=MeasureForm, extra=0, can_delete=True
)
ServiceFormSet = modelformset_factory(
    Service, form=ServiceForm, extra=0, can_delete=True
)


class TariffsForm(forms.ModelForm):
    class Meta:
        model = Tariffs
        fields = ["name", "description"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


class TariffServiceForm(forms.ModelForm):
    class Meta:
        model = TariffService
        fields = ["service", "price_per_unit"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-control service-select"}),
            "price_per_unit": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
        }


TariffServiceFormSet = inlineformset_factory(
    Tariffs, TariffService, form=TariffServiceForm, extra=0, can_delete=True
)


class PaymentDetailForm(forms.ModelForm):
    class Meta:
        model = PaymentDetail
        fields = ["name", "description"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["name", "article"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "article": forms.Select(attrs={"class": "form-control"}),
        }


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            "name",
            "address",
            "main_image",
            "image1",
            "image2",
            "image3",
            "image4",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "main_image": forms.FileInput(attrs={"class": "form-control"}),
            "image1": forms.FileInput(attrs={"class": "form-control"}),
            "image2": forms.FileInput(attrs={"class": "form-control"}),
            "image3": forms.FileInput(attrs={"class": "form-control"}),
            "image4": forms.FileInput(attrs={"class": "form-control"}),
        }


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.username


class HouseUserForm(forms.ModelForm):
    user = UserModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control useradmin-select", "prompt": "Выберите..."}
        ),
    )

    class Meta:
        model = HouseUser
        fields = ["user"]


HouseUserFormSet = inlineformset_factory(
    House, HouseUser, form=HouseUserForm, extra=0, can_delete=True
)


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


SectionFormSet = inlineformset_factory(
    House, Section, form=SectionForm, extra=0, can_delete=True
)
FloorFormSet = inlineformset_factory(
    House, Floor, form=FloorForm, extra=0, can_delete=True
)
