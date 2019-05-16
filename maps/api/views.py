from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView, CreateAPIView)

from maps.models import GeofenceLocations, LocationPoints

from .serializers import (GeofenceLocationsSerializer, LocationPointsListSerializer, LocationPointsCreateSerializer)

class GeofenceLocationsListAPIView(ListAPIView):
    queryset = GeofenceLocations.objects.all()
    serializer_class = GeofenceLocationsSerializer

    # def get_queryset(self):
    #     # return Group.objects.filter(created_by=self.request.user).filter(is_paybill=False).order_by("-id")
    #     return Group.objects.filter(is_till=True).order_by("-id")

class LocationsPointsListAPIView(ListAPIView):
    queryset = LocationPoints.objects.all()
    serializer_class = LocationPointsListSerializer

    # def get_queryset(self):
    #     # return Group.objects.filter(created_by=self.request.user).filter(is_paybill=False).order_by("-id")
    #     return Group.objects.filter(is_till=True).order_by("-id")

class LocationsPointsCreateAPIView(CreateAPIView):
    queryset = LocationPoints.objects.all()
    serializer_class = LocationPointsCreateSerializer
