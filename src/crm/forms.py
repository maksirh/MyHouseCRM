from django import forms

from src.crm.models import CallMaster
from src.house.models import Apartment
from src.user.models import Roles, User


class CallMasterCabinetForm(forms.ModelForm):
    class Meta:
        model = CallMaster
        fields = ["master_type", "apartment", "date", "time", "description"]

        widgets = {
            "master_type": forms.Select(attrs={"class": "form-control"}),
            "apartment": forms.Select(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Опишите проблему",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["apartment"].queryset = Apartment.objects.filter(owner=user)

        self.fields["master_type"].queryset = Roles.objects.filter(is_master=True)


class CabinetProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        label="Пароль",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        label="Повторити пароль",
    )

    class Meta:
        model = User
        fields = [
            "avatar",
            "last_name",
            "first_name",
            "surname",
            "birth_date",
            "phone_number",
            "viber",
            "telegram",
            "email",
            "notes",
        ]
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "form-control-file"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "viber": forms.TextInput(attrs={"class": "form-control"}),
            "telegram": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Паролі не збігаються!")
        return cleaned_data
