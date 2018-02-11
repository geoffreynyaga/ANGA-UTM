from django.contrib import admin

from .models import (Rpas,Manufacturer,RpasModel,RpasModelType,Battery,
                    PayloadModelType,PayloadModel,Payload,)


# Register your models here.


class BatteryInline(admin.StackedInline):
    model = Battery

# Register your models here.
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name','country')
    inlines = [BatteryInline,]

admin.site.register(Manufacturer, ManufacturerAdmin)

###############################################################################
class RpasAdmin(admin.ModelAdmin):
    list_display = ('rpas_nickname','rpas_serial')

admin.site.register(Rpas, RpasAdmin)

class RpasModelTypeAdmin(admin.ModelAdmin):
    list_display = ('airframe_type',)

admin.site.register(RpasModelType, RpasModelTypeAdmin)

class RpasModelAdmin(admin.ModelAdmin):
    list_display = ('model_name','weight')

admin.site.register(RpasModel, RpasModelAdmin)
###############################################################################
class BatteryAdmin(admin.ModelAdmin):
    list_display = ('batt_name','batt_number','batt_amps')

admin.site.register(Battery, BatteryAdmin)

################################################################################

class PayloadModelTypeAdmin(admin.ModelAdmin):
    list_display = ('payload_type',)

admin.site.register(PayloadModelType, PayloadModelTypeAdmin)

class PayloadModelAdmin(admin.ModelAdmin):
    list_display = ('payload_name',)

admin.site.register(PayloadModel, PayloadModelAdmin)

class PayloadAdmin(admin.ModelAdmin):
    list_display = ('payload_nickname',)

admin.site.register(Payload, PayloadAdmin)

###############################################################################
