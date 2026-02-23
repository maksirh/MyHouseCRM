from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "website/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context


class AboutUsPageView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutUsPageView, self).get_context_data(**kwargs)
        return context
