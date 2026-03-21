from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from maps.models import (
    AirportLocations,
    AirspaceFrequencies,
    AirspaceLocation,
    GeofenceLocations,
    LocationPoints,
    Obstacles,
)


class LocationPointsAdmin(LeafletGeoAdmin):
    list_display = ("name",)


admin.site.register(LocationPoints, LocationPointsAdmin)


class GeofenceLocationsAdmin(LeafletGeoAdmin):
    list_display = ("name",)


admin.site.register(GeofenceLocations, GeofenceLocationsAdmin)


class ObstaclesAdmin(LeafletGeoAdmin):
    list_display = ("description", "obstacle_type", "height")


admin.site.register(Obstacles, ObstaclesAdmin)


class AirspaceLocationAdmin(LeafletGeoAdmin):
    list_display = (
        "name",
        "icao_class",
        "upper_limit",
        "lower_limit",
        "remarks",
    )


admin.site.register(AirspaceLocation, AirspaceLocationAdmin)


class AirportLocationsAdmin(LeafletGeoAdmin):
    list_display = (
        "name",
        "icao_code",
        "elevation",
        "is_private",
        "magnetic_declination",
    )
    list_filter = ("is_private",)


admin.site.register(AirportLocations, AirportLocationsAdmin)


class AirspaceFrequenciesAdmin(LeafletGeoAdmin):
    list_display = (
        "name",
        "value",
        "is_primary",
        "public_use",
        "type_number",
    )
    list_filter = ("is_primary", "public_use")


admin.site.register(AirspaceFrequencies, AirspaceFrequenciesAdmin)
