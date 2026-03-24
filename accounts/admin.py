from django.contrib import admin

from .models import User, UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(User)
