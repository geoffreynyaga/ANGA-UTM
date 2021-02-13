from django.contrib import admin

from .models import (
    MissionWrap,
    CrewBriefing,
    BatteryLog,
    PreFlight,
    FlightLog,
    EmmergencyInfo,
    Checklist,
    ChecklistItem,
    ChecklistGroup,
)

from leaflet.admin import LeafletGeoAdmin

# from django.contrib.gis.db import OSMG
# from django.contrib.gis.db import models

# Register your models here.
# class MissionLocationAdmin(admin.ModelAdmin):
#     list_display = ('name','location')
#
# admin.site.register(MissionLocation, MissionLocationAdmin)
#
# class MissionObjectivesAdmin(admin.ModelAdmin):
#     list_display = ('objective',)

# admin.site.register(MissionObjective, MissionObjectivesAdmin)


class MissionWrapAdmin(admin.ModelAdmin):
    list_display = ("damages", "comments")


admin.site.register(MissionWrap, MissionWrapAdmin)


class CrewBriefingAdmin(admin.ModelAdmin):
    list_display = ("duties",)


admin.site.register(CrewBriefing, CrewBriefingAdmin)
############################################################################

# class SiteSurveyAdmin(admin.ModelAdmin):
#     list_display = ('location','weather')
#
# admin.site.register(SiteSurvey, SiteSurveyAdmin)


class BatteryLogAdmin(admin.ModelAdmin):
    list_display = ("end_volts",)


admin.site.register(BatteryLog, BatteryLogAdmin)


class PreFlightAdmin(admin.ModelAdmin):
    list_display = ("est_flight_time",)


admin.site.register(PreFlight, PreFlightAdmin)


class EmmergencyInfoAdmin(admin.ModelAdmin):
    list_display = ("security_service",)


admin.site.register(EmmergencyInfo, EmmergencyInfoAdmin)

###############################################################################
class FlightLogAdmin(admin.ModelAdmin):
    list_display = ("reserve_airspace",)


admin.site.register(FlightLog, FlightLogAdmin)


# from django.contrib.gis import admin as geoadmin
# admin.site.register(GeofenceLocations, geoadmin.OSMGeoAdmin)

# class MissionPathAdmin(LeafletGeoAdmin):
#     list_display = ('name',)
#
# admin.site.register(MissionPath, MissionPathAdmin)


class ChecklistAdmin(admin.ModelAdmin):
    list_display = ("rpas_model",)


admin.site.register(Checklist, ChecklistAdmin)


class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ("item_title",)


admin.site.register(ChecklistItem, ChecklistItemAdmin)


# class ChecklistGroupAdmin(admin.ModelAdmin):
#     list_display = ("title",)


# admin.site.register(ChecklistGroup, ChecklistGroupAdmin)


class MembershipInline(admin.StackedInline):
    model = ChecklistGroup.checklists.through


# class ChecklistItemAdmin(admin.ModelAdmin):
#     inlines = [
#         MembershipInline,
#     ]


# admin.site.register(ChecklistItem, ChecklistItemAdmin)


class ChecklistGroupAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    exclude = ("checklists",)


admin.site.register(ChecklistGroup, ChecklistGroupAdmin)
