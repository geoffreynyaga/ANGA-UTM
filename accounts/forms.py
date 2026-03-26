# from .models import UserProfile
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)

# User = get_user_model()
from accounts.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("phone_number", "email", "password1", "password2")
        model = User

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["phone_number"].label = "Phone Number"
            self.fields["email"].label = "Email address"


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class DeleteAccountForm(forms.Form):
    email = forms.EmailField(
        label="Confirm your email address",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email to confirm"}),
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if self.user and email != self.user.email.lower():
            raise forms.ValidationError(
                "The email address does not match your account."
            )
        return email
