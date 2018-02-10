from django.contrib import admin



from .models import Organization,OrganizationDetails


class OrganizationDetailsAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(OrganizationDetails, OrganizationDetailsAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('kcaa_no',)

admin.site.register(Organization, OrganizationAdmin)

###############################################################################