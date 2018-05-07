from django import forms

from .models import Manufacturer,Payload,Rpas
from organizations.models import Organization


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ('name', 'country')


class PayloadForm(forms.ModelForm):
    class Meta:
        model = Payload
        fields = (
        'payload_serial',
        'payload_model',
        'payload_nickname',
                
        )


class RpasCreateForm(forms.ModelForm):
    class Meta:
        model = Rpas
        fields = ('organization','rpas_nickname', 'rpas_serial', 'rpas_pic')

    def __init__(self, *args,**kwargs):
        user = kwargs.pop('rpas_user', None)  #apparently i'm popping the user from kwargs dictionary
        super(RpasCreateForm, self).__init__(*args,**kwargs)
        self.fields['organization'] = forms.ModelChoiceField(queryset=Organization.objects.filter(users=user).order_by('-id'))
