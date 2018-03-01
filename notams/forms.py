from django import forms

from .models import NotamAirspace
from leaflet.forms.widgets import LeafletWidget
from django.forms import widgets

from datetimewidget.widgets import  TimeWidget



class ExtLeafletWidget(LeafletWidget):
    geometry_field_class = 'geom'


class NotamCreateForm(forms.ModelForm):

    start_time= forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
    end= forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))

    class Meta:
        model = NotamAirspace

        fields = ( 'reason','start_day','start_time','end','geom')
        widgets = {'geom': ExtLeafletWidget(),
                    'start_day': widgets.SelectDateWidget(),

        }
