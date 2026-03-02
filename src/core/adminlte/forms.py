from django import forms
from django.forms import modelformset_factory

from src.website.models import (
    AboutUsPage,
    ContactsPage,
    Gallery,
    InfoItems,
    MainPage,
    SeoBlock,
    ServicePage,
)


class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock

        fields = ["title", "description", "keywords"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "keywords": forms.Textarea(attrs={"class": "form-control"}),
        }


class ContactsPageForm(forms.ModelForm):
    class Meta:
        model = ContactsPage

        fields = [
            "name",
            "location",
            "title",
            "email",
            "phone_number",
            "longitude",
            "latitude",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control"}),
            "latitude": forms.NumberInput(attrs={"class": "form-control"}),
        }


class InfoItemsForm(forms.ModelForm):
    class Meta:
        model = InfoItems

        fields = ["title", "description", "image"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


InfoItemsFormset = modelformset_factory(
    InfoItems, form=InfoItemsForm, extra=0, can_delete=True
)


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage

        fields = ["title", "slide1", "slide2", "slide3"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slide1": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "slide2": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "slide3": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ["image"]


GalleryFormSet = modelformset_factory(
    Gallery, form=GalleryForm, extra=1, can_delete=True
)


class AboutUsPageForm(forms.ModelForm):
    class Meta:
        model = AboutUsPage

        fields = [
            "title",
            "description",
            "director_photo",
            "additional_title",
            "additional_description",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "director_photo": forms.FileInput(attrs={"class": "form-control"}),
            "additional_title": forms.TextInput(attrs={"class": "form-control"}),
            "additional_description": forms.Textarea(attrs={"class": "form-control"}),
        }


class ServicePageForm(forms.ModelForm):
    class Meta:
        model = ServicePage
        fields = []
