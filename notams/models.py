
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.core.urlresolvers import reverse


from applications.models import ReserveAirspace
from datetime import datetime, date

from applications.validators import validate_start_date
from django.core.exceptions import ValidationError

from django.utils.safestring import mark_safe


class NotamAirspace(gis_models.Model):

    geom    = gis_models.PolygonField()
    objects = gis_models.GeoManager()


    date_created  = gis_models.DateTimeField(auto_now_add=True)
    date_modified = gis_models.DateTimeField(auto_now=True)
    start_day  = gis_models.DateField(default=date.today, validators=[validate_start_date])
    start_time = gis_models.TimeField( help_text='HH:MM:SS')
    end        = gis_models.TimeField(help_text='HH:MM:SS')

    created_by = gis_models.ForeignKey(User, on_delete=gis_models.CASCADE)
    notam_number = gis_models.CharField(max_length = 255, blank=True, null=True)

    notam_file = gis_models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)

    PENDING = 0
    ACTIVE = 1

    STATUS = (
        (PENDING,"PENDING"),
        (ACTIVE,"ACTIVE")
    )
    status = gis_models.IntegerField(default=0,choices=STATUS, blank=True, null=True)
    reason = gis_models.CharField(max_length = 255, blank=True, null=True, help_text=' Reason for NOTAM')
    centroid = gis_models.PointField(blank=True,null=True)
    expiry = gis_models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        self.centroid = self.geom.centroid
        super(NotamAirspace,self).save(*args,**kwargs)

        x = "NOTAM/KCAA/2018/"
        y = self.pk
        self.notam_number = x + str(y)

        super(NotamAirspace,self).save(*args,**kwargs)


    def clean(self):
        super(NotamAirspace, self).clean()

        if self.start_time and self.end:
            booking_time = datetime.combine(date.min, self.end) - datetime.combine(date.min, self.start_time)
            c = booking_time.total_seconds()
            if (c/3600) > 3:
                raise ValidationError('Cannot book airspace for more three hours!')
            elif (c/3600) < 0:
                raise ValidationError("You can not start a Notam at " '{:%H:%M:%S}'.format(self.start_time)  +  " and then end it at "  + '{:%H:%M:%S}'.format(self.end) )

        if self.geom:
            notam_qs    = NotamAirspace.objects.all().exclude(pk=self.pk).filter(geom__intersects=self.geom)
            reserve_qs  = ReserveAirspace.objects.filter(geom__intersects=self.geom)
            if notam_qs or reserve_qs:
                e = []
                for qs in notam_qs:
                    if  self.start_time and self.end:
                        booking_time_start = datetime.combine(self.start_day, self.start_time)
                        booking_time_end = datetime.combine(self.start_day, self.end)

                        booking_time_qs_start = datetime.combine(qs.start_day, qs.start_time)
                        booking_time_qs_end = datetime.combine(qs.start_day, qs.end)

                        if booking_time_qs_start < booking_time_start < booking_time_qs_end:
                            error = str(qs.notam_number +  " "  + "(Kindly  book after the curent NOTAM ends, try from " + qs.get_start_day + "  "+ booking_time_qs_end.strftime("%H:%M:%S")  )
                            e.append(error)

                affected = []
                for qs in reserve_qs:
                    # affected_parties = str(qs.created_by)
                    # affected.append(affected_parties)
                    if  self.start_time and self.end:

                        booking_time_qs_start = datetime.combine(qs.start_day, qs.start_time)
                        booking_time_qs_end = datetime.combine(qs.start_day, qs.end)

                        notam_start = datetime.combine(self.start_day, self.start_time)
                        notam_end = datetime.combine(self.start_day, self.end)

                        if  notam_start < booking_time_qs_start < notam_end or notam_start < booking_time_qs_end < notam_end:

                            from utm_messages.models import Notifications as n
                            n.objects.create(title = "Land Immediately",
                                             receiver = qs.created_by,
                                            )



                if e:
                    raise ValidationError(

                        ((mark_safe
                        ('Cannot book airspace in this zone!!'+
                        "You have intersected the following notam(s)  occuring at the same day and time"
                         + '<hr>' + '<p></p>'
                         + '<b>' + str(e) + '<br> '
                         + '<hr>' +  '<a href="/applications/airspace/">Go To Airspace</a>'

                         )
                         ))

                            )



    def get_area(self):
        x = self.geom.area * 12365.1613
        return x   #sq km

    def get_perimeter(self):
        x = self.geom.length
        return x*111


    def __str__(self):
    	return str(self.notam_number)

    def get_start_datetime(self):
        booking_schedule = datetime.combine(self.start_day, self.start_time)
        return booking_schedule

    def get_absolute_url(self):
        return reverse("view_airspace")


    @property
    def get_start_day(self):
        from django.contrib.humanize.templatetags.humanize import naturalday
        natural_day = naturalday(self.start_day)
        return str(natural_day)

    @property
    def get_file_url(self):
        if self.notam_file:
            file_url = self.notam_file.url
            return str(file_url)
        else:
            return str('#')
