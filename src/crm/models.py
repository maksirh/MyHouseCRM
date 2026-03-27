from django.db import models
from django.db.models import ForeignKey, ManyToManyField
from django.utils import timezone

from src.house.models import Apartment
from src.user.models import Roles, User


class PersonalAccount(models.Model):
    STATUS_CHOICES = (
        (True, "Активний"),
        (False, "Неактивний"),
    )
    number = models.CharField(
        max_length=20, unique=True, verbose_name="№", null=True, blank=True
    )
    status = models.BooleanField(
        default=True, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Залишок"
    )

    def __str__(self):
        return self.number


class Measure(models.Model):
    name = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField()


class Service(models.Model):
    name = models.CharField(null=True, max_length=50)
    measure = ForeignKey(Measure, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, blank=True, default=1
    )

    def __str__(self):
        return self.name


class Tariffs(models.Model):
    name = models.CharField()
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    services = ManyToManyField(Service, blank=True, null=True)

    def __str__(self):
        return self.name


class TariffService(models.Model):
    tariff = models.ForeignKey(Tariffs, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price_per_unit = models.FloatField()


class CounterReadings(models.Model):
    STATUSES = (
        ("new", "Нове"),
        ("included", "Враховано"),
        ("paid", "Враховано та оплачено"),
        ("zero", "Нульове"),
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="readings", null=True
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="readings", null=True
    )

    number = models.CharField(max_length=50, unique=True, null=True)
    date = models.DateField()
    meter = models.DecimalField(max_digits=10, decimal_places=1)
    status = models.CharField(choices=STATUSES, max_length=15, default="new")

    def __str__(self):
        return f"{self.service.name} - {self.apartment.number} ({self.date})"


class Receipt(models.Model):
    STATUSES = (
        ("PAID", "Оплачена"),
        ("PART", "Частково оплачена"),
        ("UNPD", "Неоплачена"),
    )

    number = models.CharField(max_length=50, unique=True, verbose_name="№ квитанції")
    apartment = models.ForeignKey(
        "house.Apartment", on_delete=models.CASCADE, verbose_name="Квартира"
    )
    tariff = models.ForeignKey(
        "crm.Tariffs", on_delete=models.SET_NULL, null=True, verbose_name="Тариф"
    )
    date = models.DateField(default=timezone.now, verbose_name="Дата створення")
    period_start = models.DateField(verbose_name="Період з", null=True, blank=True)
    period_end = models.DateField(verbose_name="Період по", null=True, blank=True)

    status = models.CharField(
        choices=STATUSES, max_length=4, default="UNPD", verbose_name="Статус"
    )
    is_made_payment = models.BooleanField(default=False, verbose_name="Проведена")
    total_sum = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Сума"
    )

    def __str__(self):
        return f"Квитанція №{self.number} від {self.date}"


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey("Service", on_delete=models.PROTECT)
    counter_reading = models.ForeignKey(
        "CounterReadings", on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class Article(models.Model):
    ARTICLE_TYPES = (("I", "Прибуток"), ("E", "Витрата"))
    name = models.CharField(max_length=128, verbose_name="Назва статті")
    article = models.CharField(choices=ARTICLE_TYPES, max_length=2, verbose_name="Тип")

    def __str__(self):
        return self.name


class CashBox(models.Model):
    number = models.CharField(
        max_length=20, unique=True, verbose_name="№ ордера", null=True, blank=True
    )
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    is_completed = models.BooleanField(default=True, verbose_name="Проведена")
    manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Менеджер"
    )

    article = models.ForeignKey(
        Article, on_delete=models.PROTECT, verbose_name="Стаття"
    )
    personal_account = models.ForeignKey(
        PersonalAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cashbox_records",
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cashbox_records",
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума")
    comment = models.TextField(null=True, blank=True, verbose_name="Коментар")

    def __str__(self):
        return f"Ордер №{self.number} від {self.date}"

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            self._update_account_balance()
            return

        old_record = CashBox.objects.get(pk=self.pk)

        if (
            old_record.is_completed
            and old_record.article.article == "I"
            and old_record.personal_account
        ):
            old_record.personal_account.balance -= old_record.amount
            old_record.personal_account.save()

        super().save(*args, **kwargs)

        self._update_account_balance()

    def _update_account_balance(self):
        if self.is_completed and self.article.article == "I" and self.personal_account:
            self.personal_account.balance += self.amount
            self.personal_account.save()

    def delete(self, *args, **kwargs):
        if self.is_completed and self.article.article == "I" and self.personal_account:
            self.personal_account.balance -= self.amount
            self.personal_account.save()
        super().delete(*args, **kwargs)


class Message(models.Model):
    sender = ForeignKey(User, on_delete=models.CASCADE, related_name="sent_message")
    title = models.TextField()
    text = models.TextField()
    date = models.DateTimeField()
    recipient = ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_message"
    )


class CallMaster(models.Model):
    STATUSES = (("N", "Нове"), ("W", "В роботі"), ("C", "Виконано"))
    status = models.CharField(choices=STATUSES, max_length=2)
    apartment = ForeignKey(Apartment, on_delete=models.CASCADE)
    master_type = ForeignKey(Roles, on_delete=models.CASCADE)
    master = ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class PaymentDetail(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    description = models.TextField(null=True, blank=True)
