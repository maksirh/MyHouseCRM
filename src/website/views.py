from django.views.generic import TemplateView

from src.website.models import AboutUsPage, MainPage


class HomePageView(TemplateView):
    template_name = "website/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        main_page = MainPage.objects.first()
        context["main_page"] = main_page

        if main_page:
            context["info_cards"] = main_page.info_card.all()
            context["seo_block"] = main_page.seo_block
            context["contact"] = main_page.contact
        else:
            context["info_cards"] = []
            context["seo_block"] = None
            context["contact"] = None

        return context


class AboutUsPageView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutUsPageView, self).get_context_data(**kwargs)

        about_page = AboutUsPage.objects.first()
        if about_page:
            context["about_page"] = about_page
        return context
