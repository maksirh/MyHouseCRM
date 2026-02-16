from django.db import models
from django.contrib.auth.models import AbstractUser


class Roles(models.Model):
    name = models.CharField()
    is_master = models.BooleanField()
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
    role = models.ForeignKey(Roles, on_delete=models.PROTECT)
    first_name = models.CharField()
    last_name = models.CharField()
    surname = models.CharField()
    birth_date = models.DateField()
    phone_number = models.CharField()
    viber = models.CharField()
    telegram = models.CharField()

