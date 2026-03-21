#!/usr/bin/env python3
# -*- coding:utf-8 -*-
##################################################################################
# File: /Users/geoff/Documents/code/ANGA-UTM/organizations/forms.py            #
# Project: organizations                                                       #
# Author: Geoffrey Nyaga  at geoffreynyagak@gmail.com                          #
# -----                                                                        #
# Last Modified: Wednesday May 1st 2024 3:23:54 pm                             #
# Modified By: Geoffrey Nyaga at geoffreynyagak@gmail.com                      #
# -----                                                                        #
# This file should not be copied and/or distributed without the express        #
# permission of Geoffrey Nyaga Kinyua                                          #
#                                                                              #
# Copyright (c) 2024 Geoffrey Nyaga Kinyua                                     #
# -----                                                                        #
# HISTORY:                                                                     #
##################################################################################
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)

User = get_user_model()
# from .models import UserProfile
from django import forms


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("phone_number", "email", "password1", "password2")
        model = User

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # self.fields["username"].label = "Display Name"
            self.fields["email"].label = "Email address"


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
