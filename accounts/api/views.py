from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rpas.models import Rpas

from accounts.api.serializers import (
    UserProfileDetailSerializer,
    UserProfileFlightLogSerializer,
    UserProfileUASListSerializer,
)
from accounts.models import UserProfile
from applications.models import ReserveAirspace

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


class UpdateExpoPushTokenAPIView(APIView):
    """Update the Expo push token for the authenticated user's profile."""

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get("expoPushToken")
        if not token:
            return Response(
                {"error": "expoPushToken is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.userprofile.expo_push_token = token
        request.user.userprofile.save(update_fields=["expo_push_token"])
        return Response({"detail": "Push token updated."}, status=status.HTTP_200_OK)
