from rest_framework_gis.serializers import GeoFeatureModelSerializer

from maps.models import GeofenceLocations, LocationPoints


class GeofenceLocationsSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = GeofenceLocations
        geo_field = "geom"
        fields = ('id', 'name', 'centroid')


class LocationPointsCreateSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = LocationPoints
        geo_field = "location"
        fields = ('id', 'name', 'IATA_shortcode', 'ICAO_shortcode', "radius", "geom")


class LocationPointsListSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = LocationPoints
        geo_field = "geom"
        fields = ('id', 'name', 'IATA_shortcode', 'ICAO_shortcode', "radius", "location")
