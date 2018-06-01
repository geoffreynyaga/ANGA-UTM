# from django.template.response import TemplateResponse
from django.shortcuts import render

from .models import Reading


def weather(request):
    data = Reading.objects.last() # TODO: Weather: Does this mean that you only get what the last user saved?
    return render(request,'weather/weather.html',{'data':data})
