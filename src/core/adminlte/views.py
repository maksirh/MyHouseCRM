from django.views.generic import TemplateView


class StatisticPageView(TemplateView):
    template_name = "adminlte/statistics.html"

    def get_context_data(self, **kwargs):
        context = super(StatisticPageView, self).get_context_data(**kwargs)
        return context
