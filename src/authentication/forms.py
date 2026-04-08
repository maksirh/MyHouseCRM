from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class CabinetLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        label="",
        error_messages={"required": "Будь ласка, підтвердіть, що ви не робот."},
    )


class AdminAuthForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        label="",
        error_messages={"required": "Будь ласка, підтвердіть, що ви не робот."},
    )

    def clean(self):
        cleaned_data = super().clean()

        user = self.get_user()

        if user is not None and not user.is_superuser:
            raise forms.ValidationError(
                "У вас немає прав доступу до панелі адміністратора.",
                code="invalid_login",
            )

        return cleaned_data
