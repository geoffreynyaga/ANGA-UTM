from django.contrib import admin

from .models import UserToUserMessages,Notifications


class UserToUserMessagesAdmin(admin.ModelAdmin):
    list_display = ('sender','receiver','title','date_created','is_read')

admin.site.register(UserToUserMessages, UserToUserMessagesAdmin)


class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('title','date_created','is_read')

admin.site.register(Notifications,NotificationsAdmin)
