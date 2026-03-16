from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.Model):
    name = models.CharField()
    is_master = models.BooleanField(default=False)
    has_statistics = models.BooleanField(default=False)
    has_cashbox = models.BooleanField(default=False)
    has_receipt = models.BooleanField(default=False)
    has_own_account = models.BooleanField(default=False)
    has_apartment = models.BooleanField(default=False)
    has_owner_apartments = models.BooleanField(default=False)
    has_message = models.BooleanField(default=False)
    has_call_master = models.BooleanField(default=False)
    has_counter = models.BooleanField(default=False)
    has_manage_site = models.BooleanField(default=False)
    has_service = models.BooleanField(default=False)
    has_tariffs = models.BooleanField(default=False)
    has_roles = models.BooleanField(default=False)
    has_user = models.BooleanField(default=False)
    has_account_detail = models.BooleanField(default=False)


class User(AbstractUser):
    STATUS_CHOICES = [
        ("active", "Активний"),
        ("new", "Новий"),
        ("disabled", "Відключений"),
    ]
    role = models.ForeignKey(Roles, on_delete=models.PROTECT, null=True)
    first_name = models.CharField(null=True, blank=True, max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    surname = models.CharField(null=True, blank=True, max_length=255)
    email = models.EmailField(null=True, blank=True, max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=255)
    viber = models.CharField(null=True, blank=True, max_length=255)
    telegram = models.CharField(null=True, blank=True, max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return self.first_name + " " + self.last_name
