from django.shortcuts import render

from django.http import HttpResponse
from django.core.serializers import serialize

from .models import LocationPoints, GeofenceLocations, Obstacles
from .forms import LocationPointsForm,ObstaclesForm

from django.views.generic import (ListView,DetailView,
                                CreateView,UpdateView,DeleteView)

def view_maps(request):
    # maps = get_object_or_404(LocationPoints)
    maps = LocationPoints.objects.all()
    return render(request, 'maps/map_details.html',{'maps':maps})

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
