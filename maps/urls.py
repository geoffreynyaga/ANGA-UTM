from django.urls import include, path, re_path

from djgeojson.views import GeoJSONLayerView

from . import views
from .models import GeofenceLocations, LocationPoints, Obstacles

urlpatterns = [
    re_path(r"^$", views.view_maps, name="view_maps"),
    # re_path(r'^locations/$', views.locations_datasets, name='locations'),
    re_path(
        r"^locations/datasets$",
        GeoJSONLayerView.as_view(
            model=LocationPoints,
            properties=(
                "name",
                "radius",
                "ICAO_shortcode",
                "IATA_shortcode",
            ),
        ),
        name="location_datasets",
    ),
    # re_path(r'^geofence/datasets$', views.geofence_datasets, name='geofence_datasets'),
    re_path(
        r"^geofence/datasets$",
        GeoJSONLayerView.as_view(model=GeofenceLocations, properties=("name",)),
        name="geofence_datasets",
    ),
    re_path(r"^geofences/$", views.view_geofences, name="view_geofences"),
    # re_path(r'^geofences/view$', views.geofence_datasets, name='geofences'),
    re_path(r"^geofences/create/$", views.LocationsCreateView.as_view(), name="create_location"),
    re_path(r"^obstacles/create/$", views.ObstaclesCreateView.as_view(), name="create_obstacles"),
    re_path(
        r"^obstacles/datasets$",
        GeoJSONLayerView.as_view(
            model=Obstacles, properties=("height", "type", "description", "obstacle_type")
        ),
        name="obstacles_datasets",
    ),
]
