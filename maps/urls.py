from django.conf.urls import url

from djgeojson.views import GeoJSONLayerView

from .models import GeofenceLocations,LocationPoints,Obstacles
from . import views

urlpatterns = [
        url(r'^$', views.view_maps, name='view_maps'),

        # url(r'^locations/$', views.locations_datasets, name='locations'),

        url(r'^locations/datasets$', GeoJSONLayerView.as_view(model=LocationPoints,
        properties=('name','radius','ICAO_shortcode','IATA_shortcode',)),
        name='location_datasets'),

        # url(r'^geofence/datasets$', views.geofence_datasets, name='geofence_datasets'),

        url(r'^geofence/datasets$', GeoJSONLayerView.as_view(model=GeofenceLocations,
        properties=('name',)),
        name='geofence_datasets'),

        url(r'^geofences/$', views.view_geofences, name='view_geofences'),

        # url(r'^geofences/view$', views.geofence_datasets, name='geofences'),

        url(r'^geofences/create/$', views.LocationsCreateView.as_view(), name='create_location'),


        url(r'^obstacles/create/$', views.ObstaclesCreateView.as_view(), name='create_obstacles'),

        url(r'^obstacles/datasets$', GeoJSONLayerView.as_view(model=Obstacles,
        properties=('height','type','description','obstacle_type')),
        name='obstacles_datasets'),

]
