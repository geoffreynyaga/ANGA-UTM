from django import forms

# from django.forms import widgets

from applications.forms import ExtLeafletWidget

from .models import LocationPoints,Obstacles


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
