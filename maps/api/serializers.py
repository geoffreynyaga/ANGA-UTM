from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoModelSerializer

from maps.models import GeofenceLocations, LocationPoints, Obstacles


class GeofenceLocationsSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    pk = serializers.SerializerMethodField()

    def get_pk(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance:
            return instance.id
        else:
            return None

    class Meta:
        model = GeofenceLocations
        geo_field = "geom"
        fields = ("id", "name", "pk", "centroid")


class LocationPointsCreateSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = LocationPoints
        geo_field = "location"
        fields = ("id", "name", "IATA_shortcode", "ICAO_shortcode", "radius", "geom")


class LocationPointsListSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = LocationPoints
        geo_field = "geom"
        fields = (
            "id",
            "name",
            "IATA_shortcode",
            "ICAO_shortcode",
            "radius",
            "location",
        )


class ObstaclesListSerializer(GeoModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = Obstacles
        geo_field = "geom"
        fields = (
            "id",
            "obstacle_type",
            "height",
            "objects",
            "description",
            "geom",
            "status",
        )
