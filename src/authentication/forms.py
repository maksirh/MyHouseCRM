from django import forms
from django.contrib.auth.forms import AuthenticationForm


class AdminAuthForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()

        user = self.get_user()

        if user is not None and not user.is_superuser:
            raise forms.ValidationError(
                "У вас немає прав доступу до панелі адміністратора.",
                code="invalid_login",
            )

        return cleaned_data
