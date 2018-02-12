# from django.template.response import TemplateResponse
from django.shortcuts import (render)
from .models import Reading

# import flightradar24

def weather(request):
    data = Reading.objects.last()
    return render(request,'weather/weather.html',{'data':data})
