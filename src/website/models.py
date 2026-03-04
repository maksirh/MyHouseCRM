from django.db import models
from django.db.models import ForeignKey, ManyToManyField
from phonenumber_field.modelfields import PhoneNumberField


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SeoBlock(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    keywords = models.TextField()


class InfoItems(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)


class Banners(models.Model):
    title = models.CharField(max_length=100)
    image1 = models.ImageField(upload_to="images/")
    image2 = models.ImageField(upload_to="images/")
    image3 = models.ImageField(upload_to="images/")


class Gallery(models.Model):
    image = models.ImageField(upload_to="gallery/")


class ContactsPage(SingletonModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    seo_block = ForeignKey(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)


class AboutUsPage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    director_photo = models.ImageField(upload_to="images/")
    gallery = ManyToManyField(Gallery, related_name="about_us_main_gallery")
    additional_title = models.CharField(max_length=100)
    additional_description = models.TextField()
    additional_gallery = ManyToManyField(
        Gallery, related_name="about_us_additional_gallery"
    )
    seo_block = ForeignKey(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)


class MainPage(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    slide1 = models.ImageField(upload_to="sliders/", null=True, blank=True)
    slide2 = models.ImageField(upload_to="sliders/", null=True, blank=True)
    slide3 = models.ImageField(upload_to="sliders/", null=True, blank=True)
    contact = ForeignKey(ContactsPage, on_delete=models.CASCADE, null=True, blank=True)
    info_card = ManyToManyField(InfoItems, null=True, blank=True)
    seo_block = ForeignKey(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)


class ServicePage(models.Model):
    service = ManyToManyField(InfoItems)
    seo_block = ForeignKey(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
