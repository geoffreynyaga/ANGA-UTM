from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView

from maps.models import AirportLocations, GeofenceLocations, LocationPoints, Obstacles

from .serializers import (
    GeofenceLocationsSerializer,
    LocationPointsCreateSerializer,
    LocationPointsListSerializer,
    ObstaclesListSerializer,
)


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


class ObstaclesListAPIView(ListAPIView):
    queryset = Obstacles.objects.all()
    serializer_class = ObstaclesListSerializer

    # def get_queryset(self):
    #     # return Group.objects.filter(created_by=self.request.user).filter(is_paybill=False).order_by("-id")
    #     return Group.objects.filter(is_till=True).order_by("-id")


def all_airports_datasets(request):
    airspace = serialize(
        "geojson",
        AirportLocations.objects.all(),
        geometry_field="boundary",
    )
    return HttpResponse(airspace, content_type="json")
