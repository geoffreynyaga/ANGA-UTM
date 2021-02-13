from rpas.models import Rpas
from django.contrib.auth.models import User
from rest_framework import generics

from accounts.api.serializers import (
    UserProfileDetailSerializer,
    UserProfileFlightLogSerializer,
    UserProfileUASListSerializer,
)
from accounts.models import UserProfile

from applications.models import ReserveAirspace

from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileDetailSerializer
    lookup_field = "pk"
    queryset = UserProfile.objects.all()


class UserProfileFlightLogsListAPIView(generics.ListAPIView):
    serializer_class = UserProfileFlightLogSerializer

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
        This view should return a list of all the uas
        for the currently authenticated user.
        """

        try:
            url_pk = self.kwargs.get("pk")
            user_from_url = User.objects.get(pk=url_pk)

            if user_from_url == self.request.user:

                queryset = Rpas.objects.filter(
                    organization=user_from_url.userprofile.organization
                ).order_by("-id")

                return queryset
            else:
                return None
        except:
            return None
