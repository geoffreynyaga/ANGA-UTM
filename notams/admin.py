from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin

from .models import NotamAirspace


class NotamAirspaceAdmin(LeafletGeoAdmin):
    list_display = ( 'notam_number', 'start_day','reason', 'created_by','expiry')

admin.site.register(NotamAirspace, NotamAirspaceAdmin)
