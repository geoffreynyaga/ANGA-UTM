from django import forms
from django.forms import widgets
from datetimewidget.widgets import TimeWidget
from leaflet.forms.widgets import LeafletWidget

from rpas.models import Rpas

from .models import ReserveAirspace


class ExtLeafletWidget(LeafletWidget):
    geometry_field_class = 'geom'


class ReserveAirspaceForm(forms.ModelForm):
    start_time = forms.TimeField(
        widget=TimeWidget(usel10n=True, bootstrap_version=3))
    end = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))

    class Meta:
        model = ReserveAirspace

        # rpas = forms.ModelMultipleChoiceField(queryset=Rpas.objects.filter(user=request.user).order_by('-id'))

        fields = ('rpas', 'start_day', 'start_time', 'end', 'geom', 'log')
        widgets = {'geom': ExtLeafletWidget(),
                   'start_day': widgets.SelectDateWidget(),

                   }

    def __init__(self, *args, **kwargs):
        # apparently i'm popping the user from kwargs dictionary
        user = kwargs.pop('user', None)
        super(ReserveAirspaceForm, self).__init__(*args, **kwargs)

        org = user.userprofile.organization

        # from organizations.models import Organization
        # org = Organization.objects.filter(users=user)
        # print(org,"this is xxxxxxxxxxxxxxxxxxx")
        """ Come up with proper queryset for all rpas in the organization for the dropdown
        """

        self.fields['rpas'] = forms.ModelChoiceField(
            queryset=Rpas.objects.filter(organization=org).order_by('-id'))


class AppliedReserveAirspaceUpdateForm(forms.ModelForm):
    class Meta:
        model = ReserveAirspace
        fields = ('rpas', 'start_day', 'start_time', 'end',
                  'geom', 'log', 'status', 'reason', 'comments')
        widgets = {'geom': LeafletWidget(),
                   'start_day': widgets.SelectDateWidget(),
                   # 'rpas': forms.widgets.Select(attrs={'readonly': True,
                   #                                       'disabled': True})
                   }

    start_time = forms.TimeField(
        widget=TimeWidget(usel10n=True, bootstrap_version=3))

    end = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))

# class LogsUploadForm(forms.ModelForm):
#     class Meta:
#         model = LogsUpload

#         fields = ('name', 'log')
#         widgets = {'geom': LeafletWidget(), }
