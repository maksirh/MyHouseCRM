from django.db import models
from django.db.models import ForeignKey, ManyToManyField

from src.crm.models import PersonalAccount, Tariffs
from src.user.models import User


class House(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField()
    main_image = models.ImageField(upload_to="images/")
    image1 = models.ImageField(upload_to="images/")
    image2 = models.ImageField(upload_to="images/")
    image3 = models.ImageField(upload_to="images/")
    image4 = models.ImageField(upload_to="images/")
    users = ManyToManyField(User)


class Section(models.Model):
    name = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Floor(models.Model):
    name = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Apartments(models.Model):
    personal_account = models.OneToOneField(PersonalAccount, on_delete=models.CASCADE)
    number = models.IntegerField()
    area = models.FloatField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    owner = ForeignKey(User, on_delete=models.CASCADE)
    tariff = ForeignKey(Tariffs, on_delete=models.CASCADE)
