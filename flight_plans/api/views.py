from flight_plans.api.serializers import (
    FlightLogListSerializer,
    FlightLogReserveAirspaceSerializer,
)
from flight_plans.models import FlightLog
from applications.models import ReserveAirspace

from rest_framework import generics


class FlightLogListAPIView(generics.ListAPIView):
    serializer_class = FlightLogListSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        # user = self.request.user
        queryset = FlightLog.objects.filter(user=self.request.user).order_by("-id")
        print(queryset, "queryset")

        return queryset
