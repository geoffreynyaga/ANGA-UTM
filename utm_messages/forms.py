from django import forms

from .models import UserToUserMessages


# from django.forms import widgets


class UserToUserMessagesForm(forms.ModelForm):
    class Meta:
        model = UserToUserMessages
        fields = ( 'receiver','title','text',)
        # widgets = {'geom': LeafletWidget(),
        #             'start_day': widgets.SelectDateWidget(),

        # }


