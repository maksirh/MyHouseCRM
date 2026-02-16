from django.db import models
from django.db.models import ManyToManyField, ForeignKey
from src.house.models import Apartments
from src.user.models import User, Roles


class Tariffs(models.Model):
    name = models.CharField()
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)


class PersonalAccount(models.Model):
    status = models.BooleanField(default=False)
    balance = models.FloatField()


class Measure(models.Model):
    name = models.CharField()


class Service(models.Model):
    name = models.CharField()
    measure = ManyToManyField(Measure)


class Currency(models.Model):
    name = models.CharField()


class TariffService(models.Model):
    tariff = models.ForeignKey(Tariffs, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    currency = models.ManyToManyField(Currency)
    price_per_unit = models.FloatField()


class Counter(models.Model):
    serial_number = models.IntegerField()
    apartment = ForeignKey(Apartments, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class CounterReadings(models.Model):
    STATUSES = (
        ("N", 'Нове'),
        ("T", 'Враховано'),
        ("Z", "Нуль")
    )
    counter = ForeignKey(Counter, on_delete=models.CASCADE)
    meter = models.FloatField()
    status = models.CharField(choices=STATUSES, max_length=2)
    date = models.DateField()


class ServiceReceipts(models.Model):
    tariff_service = models.ForeignKey(TariffService, on_delete=models.CASCADE)
    counter_reading = ForeignKey(CounterReadings, on_delete=models.CASCADE)


class Receipts(models.Model):
    STATUSES = (
        ("P", 'Оплачена'),
        ("N", 'Неоплачена'),
        ("P", 'Частково оплачена')
    )
    service_receipt = ManyToManyField(ServiceReceipts)
    apartment = ForeignKey(Apartments, on_delete=models.CASCADE)
    number = models.IntegerField()
    date = models.DateField()
    status = models.CharField(choices=STATUSES, max_length=2)
    is_made_payment = models.BooleanField(default=False)
    sum = models.FloatField()


class Article(models.Model):
    ARTICLE_TYPES = (
        ("I", "Прихід"),
        ("E", "Витрата")
    )
    name = models.CharField()
    article = models.CharField(choices=ARTICLE_TYPES, max_length=2)

class CashBox(models.Model):
    personal_account = ForeignKey(PersonalAccount, on_delete=models.CASCADE)
    cash_state = models.IntegerField()
    article = ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField()
    comment = models.TextField()
    receipts = ForeignKey(Receipts, on_delete=models.CASCADE)


class Message(models.Model):
    sender = ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    text = models.TextField()
    date = models.DateTimeField()
    recipient = ForeignKey(User, on_delete=models.CASCADE)


class CallMaster(models.Model):
    STATUSES = (
        ("N", "Нове"),
        ("W", "В роботі"),
        ("C", "Виконано")
    )
    status = models.CharField(choices=STATUSES, max_length=2)
    apartment = ForeignKey(Apartments, on_delete=models.CASCADE)
    master_type = ForeignKey(Roles, on_delete=models.CASCADE)
    master = ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


