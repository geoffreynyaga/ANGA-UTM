from django import forms

from .models import FlightLog
from applications.models import ReserveAirspace
from leaflet.forms.widgets import LeafletWidget


# class FlightLogCreateForm(forms.ModelForm):
#     class Meta:
#         model = FlightLog
#         fields = ('user','reserve_airspace','emmergency_info',
#                 'pre_flight','post_flight')

#     def __init__(self, *args,**kwargs):
#         user = kwargs.pop('user',None) #apparently i'm popping the user from kwargs dictionary
#         super(FlightLogCreateForm, self).__init__(*args,**kwargs)
#         self.fields['reserve_airspace']=forms.ModelChoiceField(queryset=ReserveAirspace.objects.filter(created_by=user).order_by('-id')[:3])

