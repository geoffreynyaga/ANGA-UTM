from datetime import datetime, date, timedelta

from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db.models import GeoManager
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.safestring import mark_safe


from maps.models import GeofenceLocations, LocationPoints

from notifications.send_a_notification import send_a_notification
from rpas.models import Rpas

from .logs import mission_planner_logs
from .validators import validate_start_date


class LogsUpload(models.Model):
     
    name = models.CharField(max_length=240)
    geom = gis_models.GeometryField(blank=True, null=True)
    log = models.FileField(
        upload_to='mission-planner-logs/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super(LogsUpload, self).save(*args, **kwargs)

        if self.log:
            from django.contrib.gis.geos import LineString, MultiLineString
            url = self.log.path
            DATA = mission_planner_logs(url)
            line = LineString(DATA)
            multi_line = MultiLineString(line)

            self.geom = multi_line

        super(LogsUpload, self).save(*args, **kwargs)


class ReserveAirspace(gis_models.Model):
    """
    This is the main model class to create reserve airspace
    it inherits from the following models
    from django.contrib.gis.db import models as gis_models
    the geom extends the models' PolgonField. Thus we can only draw polygons
    A multipolygonField would have given us ability to draw lines as well 
    """
    geom = gis_models.PolygonField(blank=True, null=True)
    
    """
         #FIX ME: Why THE FUCK DID I do blank and null?
        --FIXED: So that If log you can either upload a log or a geom
        TODO: NB:This is why documentation is very vital!!!! I'm not paid enought to write
        all the docstrings :) 
    """

    log = models.FileField(
        upload_to='mission-planner-logs/', blank=True, null=True)
    """ 
    The log field enables users to upload a Mission Planner log with extension ".waypoints"
    blank=True and null=True makes sure that user can either draw or upload a flight log. 
    This is ensured in the class' clean nethod
    """
    objects = gis_models.GeoManager()
    """
    The objects field is a modelclass manager that inherits from Geodjango's default manager
    NB: This is slightly diffrent for Django 2+ users
    """
    rpas = models.ForeignKey(Rpas)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    start_day = models.DateField(
        default=date.today, validators=[validate_start_date])
    start_time = models.TimeField(help_text='HH:MM:SS')
    end = models.TimeField(help_text='HH:MM:SS')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    PENDING = 0
    DENIED = 1
    APPROVED = 2
    STATUS = (
        (PENDING, "PENDING"),
        (DENIED, "DENIED"),
        (APPROVED, "APPROVED"),
    )

    OBJECTIVE = (
        ('TRAIN', 'Training'),
        ('MAPP', 'Mapping'),
        ('3DM', '3D Mapping'),
        ('DELV', 'Delivery'),
        ('INSP', 'Inspection'),
        ('SURV', 'Surveillance'),
        ('REC', 'Recreational'),
        ('OTH', 'Other'),

    )
    mission_type = models.CharField(
        max_length=5, choices=OBJECTIVE, null=False, default='OTH')

    application_number = models.CharField(
        max_length=255, blank=True, null=True)
    status = models.IntegerField(
        default=0, choices=STATUS, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True,
                              null=True, help_text='If Rejected: Reason for Rejecting')
    comments = models.TextField(
        blank=True, null=True, help_text='Additional Comments, if any ')
    centroid = gis_models.PointField(blank=True, null=True)
    expiry = gis_models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if self.geom:
            self.centroid = self.geom.centroid

        super(ReserveAirspace, self).save(*args, **kwargs)

        if self.log:
            from django.contrib.gis.geos import LineString, MultiLineString
            url = self.log.path
            DATA = mission_planner_logs(url)
            line = LineString(DATA)
            multi_line = MultiLineString(line)
            multi_line_to_polygon = multi_line.convex_hull
            # print(multi_line, "this is the multi line ")   Returns a multilinestring
            # print(multi_line.convex_hull, "this is the convex ")  Converts the multilinestring to polygon
            self.geom = multi_line_to_polygon
            # TODO: LOG UPLOAD: still retain the main log upload or merge the polygon to multiline string in detail_view
            
            self.centroid = self.geom.centroid

        if self.created_by.userprofile.organization.organization_type == 'ROC':
            x = "FP/KCAA/ROC/"
            y = self.pk
            self.application_number = x + str(y)

        elif self.created_by.userprofile.organization.organization_type == 'REC':
            x = "FP/KCAA/REC/"
            y = self.pk
            self.application_number = x + str(y)

        elif self.created_by.userprofile.organization.organization_type == 'PVT':
            x = "FP/KCAA/PVT/"
            y = self.pk
            self.application_number = x + str(y)

        elif self.created_by.userprofile.organization.organization_type == 'ATO':
            x = "FP/KCAA/ATO/"
            y = self.pk
            self.application_number = x + str(y)

        elif self.created_by.userprofile.organization.organization_type == 'CLB':
            x = "FP/KCAA/CLB/"
            y = self.pk
            self.application_number = x + str(y)

        # Putting saving time to be less than 6 minutes, after that model cant even add a flightlog
        saving_time = self.date_modified - self.date_created
        saving_time_seconds = saving_time.total_seconds()

        # TO DO: Questions: what if you create and save and edit in the 6 minutes?
        """ Turns out it does save two Flight Logs
        --FIXED by checking if the log is already created
        TODO: perhaps put this in properties? but can i access model properties in the clean?
        """
        if (saving_time_seconds / 60) < 6:
            from flight_plans.models import FlightLog
            get_log = FlightLog.objects.filter(reserve_airspace=self.pk)
            if not get_log:
                x = FlightLog.objects.create(
                    reserve_airspace_id=self.pk,
                    user_id=self.created_by.pk
                )
                x.save()

        # if self.status == 1:
        #     from notifications.send_a_notification import send_a_notification
        #     send_a_notification(self.created_by,"Your flight has been Rejected Flight",str(self.comments))
        #     print("should have sent a notification")
        # elif self.status == 2:
        #     from notifications.send_a_notification import send_a_notification
        #     x = mark_safe('<a href="/applications/airspace/"> Go To Airspace</a>')
        #     send_a_notification(self.created_by, x, str(self.comments))

        super(ReserveAirspace, self).save(*args, **kwargs)

    def clean(self):

        super(ReserveAirspace, self).clean()
        """ Do i really need the super method above?
        """
        if not (self.geom or self.log):
            raise ValidationError(
                "Your Geometry can't be blank. Draw an area or upload a log"
            )

        if self.start_time and self.end:
            booking_time = datetime.combine(
                date.min, self.end) - datetime.combine(date.min, self.start_time)
            c = booking_time.total_seconds()
            if (c / 3600) > 3:
                raise ValidationError(
                    'Cannot book airspace for more three hours!')
            elif (c / 3600) < 0:
                raise ValidationError("Cmon man!! You can not start a flight at " '{:%H:%M:%S}'.format(
                    self.start_time) + " and then GO BACK IN TIME to " + '{:%H:%M:%S}'.format(
                    self.end) + " to end your flight")

            booking_schedule = datetime.combine(
                self.start_day, self.start_time) - datetime.now()
            d = booking_schedule.total_seconds()
            if (d / 3600) < 4:
                four_hours_from_now = datetime.now() + timedelta(hours=4)
                raise ValidationError(
                    "Cannot book airspace less than four hours to take-off! Try from " '{:%H:%M:%S}'.format(
                        four_hours_from_now))

        if self.geom:
            from notams.models import NotamAirspace
            reserve_qs = ReserveAirspace.objects.all().exclude(
                pk=self.pk).filter(geom__intersects=self.geom)
            geo_qs = GeofenceLocations.objects.filter(
                geom__intersects=self.geom)
            airports_qs = LocationPoints.objects.filter(
                geom__intersects=self.geom)
            notams_qs = NotamAirspace.objects.filter(expiry=False).filter(
                geom__intersects=self.geom
            )
            """
                #TODO: 
                    1. ADD TIME CHECKING TO THE NOTAMS ABOVE
                    2. ADD TIME CHECK TO RESERVE_QS so that we can alert people already in flight to land, 
                        and notify those just about to fly
                        to postpone
            """
            if reserve_qs or geo_qs or airports_qs or notams_qs:
                e = []
                for qs in reserve_qs:
                    if self.start_time and self.end:
                        booking_time_start = datetime.combine(
                            self.start_day, self.start_time)
                        booking_time_end = datetime.combine(
                            self.start_day, self.end)

                        booking_time_qs_start = datetime.combine(
                            qs.start_day, qs.start_time)
                        booking_time_qs_end = datetime.combine(
                            qs.start_day, qs.end)

                        if booking_time_qs_start < booking_time_start < booking_time_qs_end:
                            error = str(
                                qs.get_name + "'s" + " " + "Airspace" + "" + "(Kindly  book after the current mission ends, try from " +
                                qs.get_start_day + "  " + booking_time_qs_end.strftime("%H:%M:%S"))
                            e.append(error)

                for qs in geo_qs:
                    error = str(qs.name)
                    e.append(error)

                for qs in airports_qs:
                    error = str(qs.name)
                    e.append(error)

                for qs in notams_qs:
                    error = str("Notam Number" + qs.notam_number)
                    e.append(error)


                if e:
                    raise ValidationError(

                        ((mark_safe
                          ('Cannot book airspace in this zone!!' +
                           "You have violed the folowing Airspace(s)"
                           + '<hr>' + '<p></p>'
                           + '<b>' + str(e) + '<br> '
                           + '<hr>' + '<a href="/applications/airspace/">Go To Airspace</a>'

                           )
                          ))

                    )
            x = self.geom.area * 12365.1613
            # geom_area = loc_obj.area_ * 12365.1613 * 10**6
            if x > 9:
                raise ValidationError(
                    'This Airspace is greater than the recommended value of 9sq km')
            #TODO: BVLOS CERTIFICATION EXEMPT

    def dist_from_airports(self):
        dis = GeofenceLocations.objects.all()
        fin = {}
        for x in dis:
            y = self.centroid.distance(x.centroid) / 111 * 10000
            if y < 15:
                fin.update({x.name: y})
        return fin

    def get_area(self):
        x = self.geom.area * 12365.1613
        return round(x, 3)  # sq km

    def get_perimeter(self):
        x = self.geom.length * 111
        return round(x, 2)  # km

    def __str__(self):
        return str(self.application_number)

    def get_start_datetime(self):
        booking_schedule = datetime.combine(self.start_day, self.start_time)
        return booking_schedule

    def get_absolute_url(self):
        return reverse("view_airspace")

    @property
    def get_rpas(self):
        return str(self.rpas.rpas_model.model_name)

    @property
    def get_name(self):
        return "%s %s" % (self.created_by.first_name, self.created_by.last_name)

    @property
    def get_phone_number(self):
        return str(self.created_by.userprofile.phone_number)

    @property
    def get_organization(self):
        return str(self.created_by.userprofile.organization.organization_details.name)

    @property
    def get_rpas_pic(self):
        return str(self.rpas.rpas_pic.url)

    @property
    def get_start_day(self):
        from django.contrib.humanize.templatetags.humanize import naturalday
        natural_day = naturalday(self.start_day)
        return str(natural_day)

    @property
    def get_airframe_type(self):
        return str(self.rpas.rpas_model.rpas_model_type)

    @property
    def get_log_completion_deadline(self):
        end_datetime = datetime.combine(self.start_day, self.end)
        deadline = end_datetime + timedelta(days=2)
        return deadline

    @property
    def get_user_profile_pic(self):
        return str(self.created_by.userprofile.profile_pic.url)
