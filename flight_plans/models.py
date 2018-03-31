from django.db import models

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from rpas.models import Battery,Rpas, RpasModel

from django.core.urlresolvers import reverse

from applications.models import ReserveAirspace

# Create your models here.

# class MissionObjective(models.Model):
#
#     OBJECTIVE = (
#             ('TRAIN', 'Training'),
#             ('MAPP', 'Mapping'),
#             ('3DM', '3D Mapping'),
#             ('DELV', 'Delivery'),
#             ('INSP', 'Inspection'),
#             ('SURV', 'Surveillance'),
#             ('REC', 'Recreational'),
#             ('OTH', 'Other'),
#
#         )
#
#     objective  = models.CharField(max_length=5, choices=OBJECTIVE, null=False)
#
#     def __str__(self):
#     	return self.get_objective_display()
#
#     def get_absolute_url(self):
#         return reverse("logs_add")


# class MissionLocation(models.Model):
#
#     name        = models.CharField(max_length = 20)
#     location    = models.CharField(max_length = 20)
#     map_location = models.PointField(srid=4326)
#     objects = models.GeoManager()
#
#     def __str__(self):
#     	return self.name
#
#     def get_absolute_url(self):
#         return reverse("logs_add")


# class SiteSurvey(models.Model):
#
#     location    = models.ForeignKey(MissionLocation,on_delete=models.CASCADE,                                )
#     weather     = models.CharField(max_length = 20)
#     # perm_letter = models.BooleanField()
#
#     def __str__(self):
#     	return self.weather

class PreFlight(models.Model):

    # take_off_time   = models.TimeField(blank=True,null=True)
    # sitesurvey      = models.ForeignKey(SiteSurvey,on_delete=models.CASCADE)
    weather         = models.CharField(max_length = 20,default='')
    altitude        = models.CharField(max_length = 20)
    est_flight_time = models.CharField(max_length = 20)
    area_size       = models.CharField(max_length = 20)
    no_of_flights   = models.CharField(max_length = 20, default = '1')
    other_info      = models.CharField(max_length=300, blank = True, null=True)
    batt_reminder   = models.CharField(max_length=10,default='')

    def __str__(self):
    	return str(self.area_size)

    def get_absolute_url(self):
        return reverse("logs_add")

class BatteryLog(models.Model):

    # flightlog = models.ForeignKey(SiteSurvey,on_delete=models.CASCADE)
    batt_number = models.ForeignKey(Battery)
    end_amps    = models.DecimalField(max_digits=5,decimal_places=1)
    end_volts   = models.CharField(max_length = 20)

    def __str__(self):
    	return self.end_volts

class CrewBriefing(models.Model):

    no_of_flights = models.IntegerField()
    duties        = models.CharField(max_length = 20)
    # tk_off_area        = models.CharField(max_length = 20)
    alt_landing_area   = models.CharField(max_length = 20)
    env_factors        = models.TextField(max_length = 20)
    air_band_radio     = models.CharField(max_length = 20)
    notam_action       = models.TextField(max_length = 20, default='None')
    copy_of_ops_pack   = models.BooleanField()
    security           = models.TextField(max_length = 300)

    def __str__(self):
    	return self.duties

class EmmergencyInfo(models.Model):

    # location       = models.ForeignKey(MissionLocation)
    closest_hosp   = models.CharField(max_length=100)
    fire_dept      = models.CharField(max_length = 20)
    nearest_police_stn = models.CharField(max_length = 20)
    security_service   = models.CharField(max_length = 20)
    other              = models.TextField(max_length = 200)

    def __str__(self):
    	return str(self.security_service)

    def get_absolute_url(self):
        return reverse("logs_add")

# class MissionPath(models.Model):
#     name = models.CharField(max_length=100)
#     path = models.MultiLineStringField()
#     objects = models.GeoManager()
#
#     def __str__(self):
#     	return self.name
#
#     def get_absolute_url(self):
#         return reverse("logs_add")

class MissionWrap(models.Model):
    # location = models.ForeignKey(MissionLocation,on_delete=models.CASCADE,default='')
    # flight_end_time    = models.CharField(max_length=20,default='')
    damages            = models.CharField(max_length = 20,blank=True,null=True)
    comments           = models.CharField(max_length=500,blank=True,null=True)
    mission_success    = models.BooleanField(default=False)
    # flight_duration    = models.DurationField()

    def __str__(self):
    	return str(self.comments)

    def get_absolute_url(self):
        return reverse("logs_list")


###############################################################################
class FlightLog(models.Model):

    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    # log_number  = models.CharField(max_length=20,default = '2017/11/', unique=True,
    #                             help_text = "2018/01/23/001")
    # purpose     = models.ForeignKey(MissionObjective,on_delete=models.CASCADE)
    reserve_airspace    = models.ForeignKey(ReserveAirspace,on_delete=models.CASCADE,blank=True,null=True)

    emmergency_info = models.ForeignKey(EmmergencyInfo,blank=True, null=True,on_delete=models.CASCADE)
    pre_flight  = models.ForeignKey(PreFlight, blank=True, null=True,on_delete=models.CASCADE)
    post_flight  = models.ForeignKey(MissionWrap,blank=True, null=True,on_delete=models.CASCADE)
    # date        = models.DateField(auto_now=False,auto_now_add=False, help_text = 'YYYY-MM-DD')
    # rpas        = models.ForeignKey(Rpas,on_delete=models.CASCADE)
    # location    = models.ForeignKey(MissionLocation,on_delete=models.CASCADE)
    # missionpath = models.ForeignKey(MissionPath,on_delete=models.CASCADE)


    def __str__(self):
    	return str(self.reserve_airspace.application_number)

    def save(self, *args, **kwargs):

        if not self.post_flight:
            x = MissionWrap.objects.create()
            x.mission_success = False
            x.save()
            self.post_flight = x

        if not self.pre_flight:
            x = PreFlight.objects.create()
            x.no_of_flights = 1
            x.save()
            self.pre_flight = x

        if not self.emmergency_info:
            x = EmmergencyInfo.objects.create()
            x.other = ""
            x.save()
            self.emmergency_info = x

        super(FlightLog,self).save(*args,**kwargs)


    def get_absolute_url(self):
        return reverse("log_detail", kwargs={"pk":self.pk})

    def get_emergency_info_pk(self):
        emmergency_info_pk = self.emmergency_info.pk
        return emmergency_info_pk

    def get_pre_flight_pk(self):
        preflight_pk = self.pre_flight.pk
        return preflight_pk

    def get_post_flight_pk(self):
        post_flight_pk = self.post_flight.pk
        return post_flight_pk

    def get_preflight_completion(self):

        est_flight_time = self.pre_flight.est_flight_time
        weather = self.pre_flight.weather
        altitude = self.pre_flight.altitude
        area_size = self.pre_flight.area_size
        no_of_flights = self.pre_flight.no_of_flights
        batt_reminder = self.pre_flight.batt_reminder
        fields = [est_flight_time,weather,altitude,area_size,no_of_flights,batt_reminder]
        initial_count = int(len(fields))
        for field in fields:
            if field == '':
                fields.remove(field)
        final_count = int(len(fields))

        progress = (final_count/initial_count)*100

        return progress



###############################################################################
class Checklist(models.Model):

    rpas_model     = models.OneToOneField(RpasModel)
    parts_check   = models.CharField(max_length=100)
    charge_status      = models.CharField(max_length = 20)
    camera_check = models.CharField(max_length = 20)
    props_check   = models.CharField(max_length = 20)
    firmware_check     = models.TextField(max_length = 200)
    camera_check = models.CharField(max_length = 20)
    risk_assesment   = models.CharField(max_length = 20)
    conditions_check     = models.TextField(max_length = 200)
    connection_check     = models.TextField(max_length = 200)

    def __str__(self):
    	return self.rpas_model.model_name

    def get_absolute_url(self):
        return reverse("checklist_detail", kwargs={"pk":self.pk})
