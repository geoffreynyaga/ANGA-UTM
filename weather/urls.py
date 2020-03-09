from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^old/$', views.weather, name='old-weather'),

    url(r'^$', views.WeatherView.as_view(), name='weather'),


    ]
