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

    manufacturer = models.ForeignKey(Manufacturer,on_delete=models.CASCADE,blank=True, null=True)
    rpas_model_type = models.ForeignKey(RpasModelType,on_delete=models.CASCADE,blank=True, null=True)

    model_name = models.CharField(max_length = 20, unique=True)
    weight = models.FloatField(blank=True, null=True)

    def __str__(self):
    	return str(self.model_name)

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_list')


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
    	return str(self.payload_type)

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_add')


class PayloadModel(models.Model):

    manufacturer = models.ForeignKey(Manufacturer,on_delete=models.CASCADE)
    payload_model_type = models.ForeignKey(PayloadModelType,on_delete=models.CASCADE)

    payload_name = models.CharField(max_length = 20, unique=True)
    payload_weight = models.CharField(max_length = 20)

    def __str__(self):
    	return str(self.payload_name)

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_add')


class Payload(models.Model):

    payload_model = models.ForeignKey(PayloadModel,on_delete=models.CASCADE,blank=True, null=True)
    payload_serial = models.CharField(max_length = 20,blank=True, null=True)
    payload_nickname = models.CharField(max_length = 20,blank=True, null=True, help_text='if any.....')

    def __str__(self):
    	return str(self.payload_serial)

    def get_absolute_url(self,*args,**kwargs):
        return reverse('rpas_list')


class Rpas(models.Model):
    user         = models.ForeignKey(User,on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE)

    rpas_model   = models.ForeignKey(RpasModel,on_delete=models.CASCADE,blank=True,null=True)
    payload      = models.ForeignKey(Payload,on_delete=models.CASCADE,blank=True,null=True)

    rpas_serial  = models.CharField(max_length = 20,unique=True)
    rpas_nickname = models.CharField(max_length = 20,blank=True,null=True,help_text="If any....e.g My Phantom Bird")

    rpas_pic = models.ImageField(upload_to = 'images/rpas')

    def __str__(self):
    	return str(self.rpas_nickname)

    def get_absolute_url(self):
        return reverse("rpas_detail", kwargs={"pk":self.pk})

    def save(self, *args, **kwargs):

        if not self.rpas_model:
            x = RpasModel.objects.create()
            x.weight = 1.0
            x.save()
            self.rpas_model = x

        if not self.payload:
            x = Payload.objects.create()
            x.payload_nickname = ''
            x.save()
            self.payload_model = x

        super(Rpas,self).save(*args,**kwargs)


    def get_absolute_url(self):
        return reverse("log_detail", kwargs={"pk":self.pk})

    def get_rpas_model_pk(self):
        rpas_model_pk = self.rpas_model.pk
        return rpas_model_pk

    def get_payload_pk(self):
        payload_pk = self.payload.pk
        return payload_pk

    def get_rpas_model_completion(self):

        manufacturer = self.rpas_model.manufacturer
        rpas_model_type = self.rpas_model.rpas_model_type
        model_name = self.rpas_model.model_name
        weight = self.rpas_model.weight

        fields = [manufacturer,rpas_model_type,model_name,weight]
        initial_count = int(len(fields))
        for field in fields:
            if field == '' or field == None:
                fields.remove(field)
        final_count = int(len(fields))
        progress = (final_count/initial_count)*100
        return round(progress,2)


    def get_payload_completion(self):

        payload_model  = self.payload.payload_model
        payload_serial = self.payload.payload_serial
        payload_nickname = self.payload.payload_nickname

        fields = [payload_model,payload_serial,payload_nickname]
        initial_count = int(len(fields))
        for field in fields:
            if field == '' or field == None:
                fields.remove(field)
        final_count = int(len(fields))
        progress = (final_count/initial_count)*100
        return round(progress,2)
