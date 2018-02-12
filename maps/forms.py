from django import forms

from .models import LocationPoints,Obstacles
from django.forms import widgets

from applications.forms import ExtLeafletWidget


class LocationPointsForm(forms.ModelForm):
    class Meta:
        model = LocationPoints
        fields = ( 'name','radius','location','ICAO_shortcode','IATA_shortcode')
        widgets = {'location': ExtLeafletWidget(),   }


class ObstaclesForm(forms.ModelForm):
    class Meta:
        model = Obstacles
        fields = ( 'obstacle_type','height','geom','description')
        widgets = {'geom': ExtLeafletWidget(),   }
