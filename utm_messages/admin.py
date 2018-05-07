from django.contrib import admin

from .models import UserToUserMessages


class UserToUserMessagesAdmin(admin.ModelAdmin):
    list_display = ('sender','receiver','title','date_created','is_read')

admin.site.register(UserToUserMessages, UserToUserMessagesAdmin)


