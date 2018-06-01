from django import forms
from django.forms import widgets

from leaflet.forms.widgets import LeafletWidget
from datetimewidget.widgets import TimeWidget

from .models import NotamAirspace


class ExtLeafletWidget(LeafletWidget):
    geometry_field_class = 'geom'


class NotamCreateForm(forms.ModelForm):
    start_time = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
    end = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))

    class Meta:
        model = NotamAirspace

        fields = ('reason', 'start_day', 'start_time', 'end', 'geom', 'notam_file')
        widgets = {'geom': ExtLeafletWidget(),
                   'start_day': widgets.SelectDateWidget(),
                   }
