from django.contrib import admin

from .models import UserToUserMessages


class UserToUserMessagesAdmin(admin.ModelAdmin):
    list_display = ('sender','receiver','title','date_created')

admin.site.register(UserToUserMessages, UserToUserMessagesAdmin)
