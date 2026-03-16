from django.db import models
from django.db.models import ForeignKey, ManyToManyField

from src.user.models import User


class House(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to="images/", null=True, blank=True)
    image1 = models.ImageField(upload_to="images/", null=True, blank=True)
    image2 = models.ImageField(upload_to="images/", null=True, blank=True)
    image3 = models.ImageField(upload_to="images/", null=True, blank=True)
    image4 = models.ImageField(upload_to="images/", null=True, blank=True)
    users = ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Floor(models.Model):
    name = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    account = models.ForeignKey(
        "crm.PersonalAccount", on_delete=models.CASCADE, null=True, blank=True
    )
    number = models.IntegerField()
    area = models.DecimalField(max_digits=7, decimal_places=2)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, blank=True
    )
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, blank=True)
    owner = ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tariff = models.ForeignKey(
        "crm.Tariffs", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return str(self.number)


class HouseUser(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
