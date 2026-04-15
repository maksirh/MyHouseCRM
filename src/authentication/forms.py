from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from src.crm.models import PersonalAccount

User = get_user_model()


class CabinetRegistrationForm(forms.ModelForm):
    account_number = forms.CharField(
        label="Особовий рахунок",
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "00000-00000"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        ),
    )
    password_confirm = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Повторіть пароль"}
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ім'я"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Прізвище"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Телефон"}
            ),
        }

    def clean_account_number(self):
        acc_num = self.cleaned_data.get("account_number")
        if not PersonalAccount.objects.filter(number=acc_num).exists():
            raise forms.ValidationError(
                "Особовий рахунок не знайдено. Перевірте правильність вводу."
            )
        return acc_num

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get("password")
        pw_conf = cleaned_data.get("password_confirm")
        if pw and pw_conf and pw != pw_conf:
            self.add_error("password_confirm", "Паролі не співпадають.")
        return cleaned_data


class CabinetLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        label="",
        error_messages={"required": "Будь ласка, підтвердіть, що ви не робот."},
    )

    def clean(self):
        cleaned_data = super().clean()
        user = self.get_user()

        if user is not None and user.is_staff:
            raise forms.ValidationError(
                "Персоналу вхід через панель адміністратора.",
                code="invalid_login",
            )
        return cleaned_data


class AdminAuthForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        label="",
        error_messages={"required": "Будь ласка, підтвердіть, що ви не робот."},
    )

    def clean(self):
        cleaned_data = super().clean()
        user = self.get_user()

        if user is not None and not (user.is_staff or user.is_superuser):
            raise forms.ValidationError(
                "У вас немає прав доступу до панелі адміністратора.",
                code="invalid_login",
            )
        return cleaned_data
