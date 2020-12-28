#!/usr/bin/env python3
# -*- coding:utf-8 -*-
##################################################################################
# File: /mnt/c/Projects/ANGA UTM/src/accounts/api/views.py                       #
# Project: MFUKO                                                                 #
# Author: Geoffrey Nyaga Kinyua  at geoffrey@mfuko.co.ke                         #
# -----                                                                          #
# Last Modified: Monday December 28th 2020 9:54:58 pm                            #
# Modified By: Geoffrey Nyaga Kinyua at geoffrey@mfuko.co.ke                     #
# -----                                                                          #
# This file should not be copied and/or distributed without the express          #
# permission of MFUKO PAYMENTS SERVICES Ltd.                                     #
#                                                                                #
# Copyright (c) 2020 MFUKO PAYMENTS SERVICES Ltd.                                #
# -----                                                                          #
# HISTORY:                                                                       #
##################################################################################
# class ViewProfile(LoginRequiredMixin, generic.DetailView):
#     template_name = "accounts/profile.html"
#     model = UserProfile

#     def get_context_data(self, *args, **kwargs):
#         context = super(ViewProfile, self).get_context_data(**kwargs)
#         pk = self.kwargs["pk"]
#         thisuser = User.objects.get(pk=pk)
#         org = thisuser.userprofile.organization
#         context["myrpas"] = Rpas.objects.filter(organization=org)
#         context["myflightlogs"] = FlightLog.objects.filter(user=thisuser)
#         return context

from rpas.models import Rpas
from django.contrib.auth.models import User
from rest_framework import generics

from accounts.api.serializers import (
    UserProfileDetailSerializer,
    UserProfileFlightLogSerializer,
    UserProfileUASListSerializer,
)
from accounts.models import UserProfile
from flight_plans.api.serializers import (
    FlightLogListSerializer,
    FlightLogReserveAirspaceSerializer,
)
from flight_plans.models import FlightLog
from applications.models import ReserveAirspace

from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileDetailSerializer
    lookup_field = "pk"
    queryset = UserProfile.objects.all()


class UserProfileFlightLogsListAPIView(generics.ListAPIView):
    serializer_class = UserProfileFlightLogSerializer
    # lookup_field = "pk"

    def get_queryset(self):
        """
        This view should return a list of all the logs
        for the currently authenticated user.
        """

        try:
            url_pk = self.kwargs.get("pk")
            user_from_url = User.objects.get(pk=url_pk)
            if user_from_url == self.request.user:

                queryset = ReserveAirspace.objects.filter(
                    created_by=self.request.user
                ).order_by("-id")

                return queryset
            else:
                return None
        except:
            return None


class UserProfileUASListAPIView(generics.ListAPIView):
    serializer_class = UserProfileUASListSerializer

    def get_queryset(self):
        """
        This view should return a list of all the logs
        for the currently authenticated user.
        """

        try:
            url_pk = self.kwargs.get("pk")
            user_from_url = User.objects.get(pk=url_pk)

            # thisuser = User.objects.get(pk=pk)
            # org = thisuser.userprofile.organization
            # Rpas.objects.filter(organization=org)

            if user_from_url == self.request.user:

                queryset = Rpas.objects.filter(
                    organization=user_from_url.userprofile.organization
                ).order_by("-id")

                return queryset
            else:
                return None
        except:
            return None
