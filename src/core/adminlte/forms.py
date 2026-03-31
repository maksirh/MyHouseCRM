from django import forms
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory

from src.crm.models import (
    Article,
    CallMaster,
    CashBox,
    CounterReadings,
    Measure,
    PaymentDetail,
    PersonalAccount,
    Receipt,
    ReceiptItem,
    Service,
    Tariffs,
    TariffService,
)
from src.house.models import Apartment, Floor, House, HouseUser, Section
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


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ["number", "area", "house", "section", "floor", "owner", "tariff"]
        widgets = {
            "number": forms.NumberInput(attrs={"class": "form-control"}),
            "area": forms.NumberInput(attrs={"class": "form-control"}),
            "house": forms.Select(attrs={"class": "form-control"}),
            "section": forms.Select(attrs={"class": "form-control"}),
            "floor": forms.Select(attrs={"class": "form-control"}),
            "owner": forms.Select(attrs={"class": "form-control"}),
            "tariff": forms.Select(attrs={"class": "form-control"}),
        }


class PersonalAccountForm(forms.ModelForm):
    house = forms.ModelChoiceField(
        queryset=House.objects.all(),
        required=False,
        empty_label="Оберіть...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        required=False,
        empty_label="Оберіть...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    apartment = forms.ModelChoiceField(
        queryset=Apartment.objects.all(),
        required=False,
        empty_label="Оберіть...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = PersonalAccount
        fields = ["number", "status"]

        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class CounterReadingForm(forms.ModelForm):
    house = forms.ModelChoiceField(
        queryset=House.objects.all(), required=False, empty_label="Выберите..."
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(), required=False, empty_label="Выберите..."
    )

    class Meta:
        model = CounterReadings
        fields = ["number", "date", "status", "apartment", "service", "meter"]

        widgets = {
            "date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ReceiptForm(forms.ModelForm):
    house = forms.ModelChoiceField(
        queryset=House.objects.all(), required=False, empty_label="Оберіть..."
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(), required=False, empty_label="Оберіть..."
    )

    class Meta:
        model = Receipt
        fields = [
            "number",
            "date",
            "status",
            "is_made_payment",
            "apartment",
            "tariff",
            "period_start",
            "period_end",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "period_start": forms.DateInput(attrs={"type": "date"}),
            "period_end": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
        self.fields["is_made_payment"].widget.attrs["class"] = ""


class ReceiptItemForm(forms.ModelForm):
    class Meta:
        model = ReceiptItem
        fields = ["service", "quantity", "price_per_unit", "total_price"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-control service-select"}),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control quantity-input", "step": "0.01"}
            ),
            "price_per_unit": forms.NumberInput(
                attrs={"class": "form-control price-input", "step": "0.01"}
            ),
            "total_price": forms.NumberInput(
                attrs={"class": "form-control total-input", "readonly": True}
            ),
        }


ReceiptItemFormSet = inlineformset_factory(
    Receipt, ReceiptItem, form=ReceiptItemForm, extra=1, can_delete=True
)


class CashBoxIncomeForm(forms.ModelForm):
    class Meta:
        model = CashBox
        fields = [
            "number",
            "date",
            "is_completed",
            "manager",
            "personal_account",
            "article",
            "amount",
            "comment",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["article"].queryset = Article.objects.filter(article="I")


class CashBoxExpenseForm(forms.ModelForm):
    class Meta:
        model = CashBox
        fields = [
            "number",
            "date",
            "is_completed",
            "manager",
            "article",
            "amount",
            "comment",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["article"].queryset = Article.objects.filter(article="E")


class CallMasterForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Власник квартири",
    )

    class Meta:
        model = CallMaster
        fields = [
            "date",
            "time",
            "owner",
            "apartment",
            "master_type",
            "master",
            "status",
            "description",
            "comment",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "apartment": forms.Select(attrs={"class": "form-control"}),
            "master_type": forms.Select(attrs={"class": "form-control"}),
            "master": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "comment": forms.Textarea(attrs={"class": "form-control summernote"}),
        }
