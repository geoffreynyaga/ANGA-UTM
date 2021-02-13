from flight_plans.api.serializers import (
    CheckListAllSerializer,
    CheckListDetailSerializer,
    FlightLogListSerializer,
    FlightLogReserveAirspaceSerializer,
)
from flight_plans.models import ChecklistGroup, FlightLog
from applications.models import ReserveAirspace

from rest_framework import generics


class FlightLogListAPIView(generics.ListAPIView):
    serializer_class = FlightLogListSerializer

    def get_queryset(self):
        """
        This view should return a list of all the logs
        for the currently authenticated user.
        """
        queryset = FlightLog.objects.filter(user=self.request.user).order_by("-id")

        return queryset


class CheckListDetailAPIView(generics.RetrieveAPIView):
    queryset = ChecklistGroup.objects.all()
    serializer_class = CheckListDetailSerializer
    lookup_field = "pk"


class CheckListAllAPIView(generics.ListAPIView):
    serializer_class = CheckListAllSerializer
    queryset = ChecklistGroup.objects.all()

