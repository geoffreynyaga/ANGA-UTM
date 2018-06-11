# from django.template.response import TemplateResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import Reading


def weather(request):
    data = Reading.objects.last() 
    # TODO: Weather: Does this mean that you only get what the last user saved?
    return render(request,'weather/weather.html',{'data':data})


class WeatherView(TemplateView):

    template_name = "weather/weather-js.html"

    # def get_context_data(self, **kwargs):
    #     context = super(HomePageView, self).get_context_data(**kwargs)
    #     context['latest_articles'] = Article.objects.all()[:5]
    #     return context
