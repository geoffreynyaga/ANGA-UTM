from django.db import models
from django.db.models import Manager as GeoManager
from django.contrib.gis.db import models as gis_models

# from djgeojson.fields import PolygonField


class LocationPoints(gis_models.Model):
    name = gis_models.CharField(max_length=120)
    IATA_shortcode = gis_models.CharField(
        max_length=3,
        blank=True,
        null=True,
        help_text="NBO (for JKIA Nairobi)",
        unique=True,
    )
    ICAO_shortcode = gis_models.CharField(
        max_length=4,
        blank=True,
        null=True,
        help_text="HKJK for (JOMO Kenyatta)",
        unique=True,
    )

    radius = models.FloatField(default=5, help_text="km")
    geom = gis_models.PolygonField(blank=True, null=True)
    location = gis_models.PointField()

    objects = GeoManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        center = self.location
        radius = self.radius * 0.008
        circle = center.buffer(radius)
        self.geom = circle
        super().save(*args, **kwargs)


class GeofenceLocations(gis_models.Model):
    name = gis_models.CharField(max_length=20)
    geom = gis_models.PolygonField(srid=4326)
    objects = GeoManager()
    centroid = gis_models.PointField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.centroid = self.geom.centroid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Obstacles(gis_models.Model):

    OBSTACLE_TYPE = (
        ("PWL", "Power Lines"),
        ("TRS", "Trees"),
        ("BLD", "Building"),
        ("TWR", "Tower"),
    )

    obstacle_type = models.CharField(max_length=4, choices=OBSTACLE_TYPE, null=False)
    height = models.FloatField(help_text="estimated height in meters")
    objects = GeoManager()
    description = models.CharField(max_length=120, blank=True, null=True)
    geom = gis_models.GeometryField()
    status = gis_models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.geom.geom_type == "Point":
            center = self.geom
            radius = (15 * 0.008) / 1000
            circle = center.buffer(radius)
            self.geom = circle
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_obstacle_type_display()

    @property
    def type(self):
        return str(self.get_obstacle_type_display())
