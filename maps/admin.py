from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin

from .models import LocationPoints,GeofenceLocations,Obstacles

class LocationPointsAdmin(LeafletGeoAdmin):
    list_display = ('name',)

admin.site.register(LocationPoints, LocationPointsAdmin)


class GeofenceLocationsAdmin(LeafletGeoAdmin):
    list_display = ('name',)

admin.site.register(GeofenceLocations, GeofenceLocationsAdmin)


class ObstaclesAdmin(LeafletGeoAdmin):
    list_display = ('description','obstacle_type','height')

admin.site.register(Obstacles, ObstaclesAdmin)
