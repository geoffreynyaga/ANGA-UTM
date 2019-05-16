from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
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
        # print(user, "this is the init user")

        self.user = user
        """ I have done this to ALSO pass the user above to the self (Form) so that I can access
        the user in other functions below like clean. NB: I can not 'pop' the user all the time (and it doesnt work btw)
        """

        super(ReserveAirspaceForm, self).__init__(*args, **kwargs)

        org = user.userprofile.organization
        # from organizations.models import Organization
        # org = Organization.objects.filter(users=user)
        # print(org,"this is xxxxxxxxxxxxxxxxxxx")
        """ Come up with proper queryset for all rpas in the organization for the dropdown
        """
        self.fields['rpas'] = forms.ModelChoiceField(
            queryset=Rpas.objects.filter(organization=org).order_by('-id'))

        """
        TO DO: Restrict User to not make two flight times at the same hour at different locations
        --FIXED
        Also fixed the amount of flights somebody can book in a day

        #TODO: Settings DASHBOARD FOR KCAA TO SET Max number of flights, max un-approved flights,max area,
               max
        """
    def clean(self, *args, **kwargs):

        cleaned_data = super(ReserveAirspaceForm, self).clean(*args, **kwargs)
        user = self.user #this was passed in the __init__ function above
        # print(user,"this is user")

        start_day = cleaned_data.get('start_day')
        start_time = cleaned_data.get('start_time')
        end = cleaned_data.get('end')
        # print(start_day, "this is cleaned data start day")
        # print(start_time, "this is cleaned data start_time")

        if start_day and start_time:
            other_user_flights_on_the_day = ReserveAirspace.objects.filter(created_by=user).filter(start_day=start_day)
            # print(other_user_flights_on_the_day,"other Flights that day")
            if other_user_flights_on_the_day.count() >= 2:
                self.add_error(None, ValidationError('You have already booked 2 flights for this day, That is the max allowed'))

            other_user_flights_on_that_time = other_user_flights_on_the_day.filter(
                start_time__gte=start_time).filter(end__lte=end)

            if other_user_flights_on_that_time.count() >= 0:
                for flight in other_user_flights_on_that_time:

                    self.add_error(None, ValidationError(
                    f"You have already booked another flight(s) {flight} at the same time" )
                    )
            # print(other_user_flights_on_that_time, "other_user_flights_on_that_time")

        return cleaned_data



class AppliedReserveAirspaceUpdateForm(forms.ModelForm):
    class Meta:
        model = ReserveAirspace
        fields = ('rpas', 'start_day', 'start_time', 'end',
                  'geom', 'log', )
        widgets = {'geom': LeafletWidget(),
                   'start_day': widgets.SelectDateWidget(),
                   # 'rpas': forms.widgets.Select(attrs={'readonly': True,
                   #                                       'disabled': True})
                   }

    start_time = forms.TimeField(
        widget=TimeWidget(usel10n=True, bootstrap_version=3))

    end = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AppliedReserveAirspaceUpdateForm, self).__init__(*args, **kwargs)
        org = user.userprofile.organization
        self.fields['rpas'] = forms.ModelChoiceField(
            queryset=Rpas.objects.filter(organization=org).order_by('-id'))


class CAAAppliedReserveAirspaceUpdateForm(forms.ModelForm):
    class Meta:
        model = ReserveAirspace
        fields = ( 'start_day', 'start_time', 'end',
                  'geom', 'status', 'reason', 'comments')
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
