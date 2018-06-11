from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin

from .models import ReserveAirspace, LogsUpload


# Register your models here.

class ReserveAirspaceAdmin(LeafletGeoAdmin):
    list_display = ('created_by', 'application_number','status',
                    'expiry', 'get_start_datetime', 'comments')

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance

admin.site.register(ReserveAirspace, ReserveAirspaceAdmin)


class LogsUploadAdmin(LeafletGeoAdmin):
    list_display = ('name',)

admin.site.register(LogsUpload, LogsUploadAdmin)
