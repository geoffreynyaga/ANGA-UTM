from django.shortcuts import render

from django.core.serializers import serialize
from django.http import HttpResponse
from django.views.generic import CreateView

from .forms import LocationPointsForm,ObstaclesForm
from .models import LocationPoints, GeofenceLocations, Obstacles


def view_maps(request):
    # maps = get_object_or_404(LocationPoints)
    maps = LocationPoints.objects.all()
    return render(request, 'maps/map_details.html',{'maps':maps}) #FIXME: map_details.html not found


def locations_datasets(request):
    locations = serialize('geojson', LocationPoints.objects.all())
    return HttpResponse(locations, content_type='json')


class LocationsCreateView(CreateView):
    form_class = LocationPointsForm
    template_name = 'maps/create_locations.html'
    success_url = '/applications/airspace'


def view_geofences(request):
    maps = LocationPoints.objects.all()
    return render(request, 'maps/geofences.html',{'maps':maps})


def geofence_datasets(request):
    geofence = serialize('geojson', GeofenceLocations.objects.all())
    return HttpResponse(geofence, content_type='json')


class ObstaclesCreateView(CreateView):
    form_class = ObstaclesForm
    template_name = 'maps/create_obstacles.html'
    success_url = '/applications/airspace'


def obstacles_datasets(request):
    obstacles = serialize('geojson', Obstacles.objects.all())
    return HttpResponse(obstacles, content_type='json')
