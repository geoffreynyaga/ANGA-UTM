from django.urls import include, path, re_path

from . import views

urlpatterns = [
    re_path(r"^old/$", views.weather, name="old-weather"),
    re_path(r"^$", views.WeatherView.as_view(), name="weather"),
]
