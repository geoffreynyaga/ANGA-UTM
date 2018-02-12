from django import forms

from .models import MissionObjective,MissionPath
from leaflet.forms.widgets import LeafletWidget

class MissionObjectiveForm(forms.ModelForm):
    class Meta:

        model = MissionObjective

        fields = (
        'objective',
        )


class MissionPathForm(forms.ModelForm):
    class Meta:
        model = MissionPath
        fields = ('name', 'path')
        widgets = {'path': LeafletWidget()}
