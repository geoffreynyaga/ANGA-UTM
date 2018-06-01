from django.contrib import admin

from .models import Organization,OrganizationDetails,PostHolder


class OrganizationDetailsAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(OrganizationDetails, OrganizationDetailsAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_details','kcaa_no','organization_type')

admin.site.register(Organization, OrganizationAdmin)

###############################################################################


class PostHolderAdmin(admin.ModelAdmin):
    list_display = ('user','organization','role')

admin.site.register(PostHolder, PostHolderAdmin)