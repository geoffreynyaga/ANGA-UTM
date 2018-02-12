from django import forms

# from django.contrib.admin import widgets
from .models import ReserveAirspace,LogsUpload
from leaflet.forms.widgets import LeafletWidget
# from leaflet.forms.fields import PolygonField
from django.forms import widgets

from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget



class ExtLeafletWidget(LeafletWidget):
    geometry_field_class = 'geom'


class ReserveAirspaceForm(forms.ModelForm):

    start_time= forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
    end= forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))

    class Meta:
        model = ReserveAirspace

        fields = ( 'rpas','start_day','start_time','end','geom')
        widgets = {'geom': ExtLeafletWidget(),
                    'start_day': widgets.SelectDateWidget(),

        }


class AppliedReserveAirspaceUpdateForm(forms.ModelForm):
    class Meta:
        model = ReserveAirspace
        fields = ( 'rpas','start_day','start_time','end','geom','status','reason','comments')
        widgets = {'geom': LeafletWidget(),
                    'start_day': widgets.SelectDateWidget(),
                    # 'rpas': forms.widgets.Select(attrs={'readonly': True,
                    #                                       'disabled': True})

        }
    start_time= forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))

    end= forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))


class LogsUploadForm(forms.ModelForm):
    class Meta:
        model = LogsUpload

        fields = ( 'name','geom','log')
        widgets = {'geom': LeafletWidget(),


        }
