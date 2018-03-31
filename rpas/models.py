from django.db import models

from django.contrib.auth.models import User

# from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

from django.utils import timezone

from organizations.models import Organization




class Manufacturer(models.Model):

    name = models.CharField(max_length = 20, unique=True)
    country = models.CharField(max_length = 20)
    logo = models.ImageField(upload_to = 'images/logo/manufacturer',  blank=True, null=True)

    def __str__(self):
    	return self.name

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_add')


class RpasModelType(models.Model):

    AIRFRAME_TYPE = (
            ('PLANE', 'PLANE'),
            ('QUAD', 'QUADCOPTER'),
            ('HEXA', 'HEXACOPTER'),
            ('TRI', 'TRICOPTER'),
            ('OCTA', 'OCTACOPTER'),
            ('VTOL', 'VTOL'),
        )
    airframe_type = models.CharField(max_length=5, choices=AIRFRAME_TYPE,null=False)

    def __str__(self):
    	return self.get_airframe_type_display()

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_add')


class RpasModel(models.Model):

    manufacturer = models.ForeignKey(Manufacturer,on_delete=models.CASCADE)
    rpas_model_type = models.ForeignKey(RpasModelType,on_delete=models.CASCADE)

    model_name = models.CharField(max_length = 20, unique=True)
    weight = models.CharField(max_length = 20)

    def __str__(self):
    	return self.model_name

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_add')


class Battery(models.Model):

    manufacturer = models.ForeignKey(Manufacturer,on_delete=models.CASCADE)
    batt_name = models.CharField(max_length = 20, unique=True)
    batt_volts = models.CharField(max_length = 20)
    batt_amps = models.CharField(max_length = 20)
    batt_number = models.IntegerField()

    def __str__(self):
    	return self.batt_name

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_add')


class PayloadModelType(models.Model):

    PAYLOAD_TYPE = (
            ('RBG', 'RGB CAMERA'),
            ('MSTL', 'MULTISPECTRAL'),
            ('HYPL', 'HYPERSPECTRAL'),
            ('FPV', 'FPV'),
            ('SURV', 'SURVIELANCE'),
            ('VTOL', 'VTOL'),
            ('IFR', 'INFRA-RED'),
        )
    payload_type = models.CharField(max_length=5, choices=PAYLOAD_TYPE,null=False)

    def __str__(self):
    	return self.payload_type

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_add')


class PayloadModel(models.Model):

    manufacturer = models.ForeignKey(Manufacturer,on_delete=models.CASCADE)
    payload_model_type = models.ForeignKey(PayloadModelType,on_delete=models.CASCADE)

    payload_name = models.CharField(max_length = 20, unique=True)
    payload_weight = models.CharField(max_length = 20)

    def __str__(self):
    	return self.payload_name

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_add')


class Payload(models.Model):

    manufacturer = models.ForeignKey(Manufacturer,on_delete=models.CASCADE)
    payload_model = models.ForeignKey(PayloadModel,on_delete=models.CASCADE)
    payload_serial = models.CharField(max_length = 20)
    payload_nickname = models.CharField(max_length = 20)

    def __str__(self):
    	return self.payload_nickname

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_add')


class Rpas(models.Model):
    user         = models.ForeignKey(User,on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE)
    rpas_model   = models.ForeignKey(RpasModel,on_delete=models.CASCADE)
    payload      = models.ForeignKey(Payload,on_delete=models.CASCADE)
    rpas_serial  = models.CharField(max_length = 20)
    rpas_nickname = models.CharField(max_length = 20)
    rpas_pic = models.ImageField(upload_to = 'images/rpas')

    def __str__(self):
    	return self.rpas_nickname

    def get_absolute_url(self):
        return reverse("rpas_detail", kwargs={"pk":self.pk})
