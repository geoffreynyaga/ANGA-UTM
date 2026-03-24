from django.contrib.gis.db import models as gis_models
from django.db import models
from django.db.models import Manager as GeoManager

# from djgeojson.fields import PolygonField


class LocationPoints(gis_models.Model):
    class Meta:
        """Meta definition for LocationPoints."""

        verbose_name = "Location Point"
        verbose_name_plural = "Location Points"

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
    class Meta:
        """Meta definition for GeofenceLocations."""

        verbose_name = "Geofence Location"
        verbose_name_plural = "Geofence Locations"

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
    class Meta:
        """Meta definition for Obstacles."""

        verbose_name = "Obstacle"
        verbose_name_plural = "Obstacles"

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


class AirspaceFrequencies(models.Model):
    class Meta:
        ordering = ["-value"]

    value = models.FloatField()
    name = models.CharField(
        max_length=255,
    )
    is_primary = models.BooleanField(default=False)
    public_use = models.BooleanField(default=False)

    type_number = models.IntegerField()

    def __str__(self):
        return self.name + str(self.value)


class AirspaceLocation(gis_models.Model):
    class Meta:
        """Meta definition for AirspaceLocation."""

        verbose_name = "Airspace Location"
        verbose_name_plural = "Airspace Locations"

    name = models.CharField(max_length=120)
    geom = gis_models.PolygonField(srid=4326)
    centroid = gis_models.PointField(blank=True, null=True)
    objects = GeoManager()

    icao_class = models.IntegerField(blank=True, null=True)
    upper_limit = models.IntegerField(blank=True, null=True)
    upper_limit_unit = models.IntegerField(blank=False, null=True)
    lower_limit = models.IntegerField(blank=True, null=True)
    lower_limit_unit = models.IntegerField(blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.centroid = self.geom.centroid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AirportLocations(gis_models.Model):
    class Meta:
        """Meta definition for AirportLocations."""

        verbose_name = "Airport Location"
        verbose_name_plural = "Airport Locations"

    name = models.CharField(max_length=200)
    icao_code = models.CharField(max_length=10, blank=True, null=True)
    elevation = models.FloatField(default=0.0)

    # geom = gis_models.PointField(srid=4326)
    boundary = gis_models.PolygonField(srid=4326, blank=True, null=True)
    radius = models.FloatField(default=10, help_text="km")  # km
    centroid = gis_models.PointField(blank=True, null=True)

    objects = GeoManager()

    is_private = models.BooleanField(default=False)
    magnetic_declination = models.FloatField(default=0.0)
    airspace_frequencies = models.ManyToManyField(AirspaceFrequencies, blank=True)

    def save(self, *args, **kwargs):
        center = self.centroid
        radius = self.radius * 0.008
        circle = center.buffer(radius)
        self.boundary = circle
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
