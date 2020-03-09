from django import forms

from .models import UserToUserMessages


class UserToUserMessagesForm(forms.ModelForm):
    class Meta:
        model = UserToUserMessages
        fields = ('receiver', 'title', 'text', )
