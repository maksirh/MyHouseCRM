from django import forms

from src.crm.models import CallMaster
from src.house.models import Apartment
from src.user.models import Roles


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
