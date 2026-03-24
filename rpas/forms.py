from django import forms

from organizations.models import Organization

from .models import Manufacturer, Payload, Rpas


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ("name", "country")


class PayloadForm(forms.ModelForm):
    class Meta:
        model = Payload
        fields = (
            "payload_serial",
            "payload_model",
            "payload_nickname",
        )


class RpasCreateForm(forms.ModelForm):
    class Meta:
        model = Rpas
        fields = ( "cor_number", "rpas_serial", "rpas_nickname","rpas_pic")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop(
            "rpas_user", None
        )  # apparently i'm popping the user from kwargs dictionary
        super(RpasCreateForm, self).__init__(*args, **kwargs)
