from django.db import models
from django.db.models import ForeignKey, ManyToManyField
from phonenumber_field.modelfields import PhoneNumberField

class SeoBlock(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    keywords = models.TextField()


class InfoItems(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')


class Banners(models.Model):
    title = models.CharField(max_length=100)
    image1 = models.ImageField(upload_to='images/')
    image2 = models.ImageField(upload_to='images/')
    image3 = models.ImageField(upload_to='images/')


class Gallery(models.Model):
    image = models.ImageField(upload_to='images/')


class ContactsPage(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = PhoneNumberField(blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    seo_block = ForeignKey(SeoBlock, on_delete=models.CASCADE)


class AboutUsPage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    director_photo = models.ImageField(upload_to='images/')
    gallery = ManyToManyField(Gallery)
    additional_title = models.CharField(max_length=100)
    additional_description = models.TextField()
    additional_gallery = ManyToManyField(Gallery)
    seo_bloc = ForeignKey(SeoBlock, on_delete=models.CASCADE)


class MainPage(models.Model):
    title = models.CharField(max_length=100)
    banner = ForeignKey(Banners, on_delete=models.CASCADE)
    contact = ForeignKey(ContactsPage, on_delete=models.CASCADE)
    info_card = ForeignKey(InfoItems, on_delete=models.CASCADE)
    seo_block = ForeignKey(SeoBlock, on_delete=models.CASCADE)


class ServicePage(models.Model):
    service = ManyToManyField(InfoItems)
    seo_block = ForeignKey(SeoBlock, on_delete=models.CASCADE)

