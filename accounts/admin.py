from django.contrib import admin

from .models import User, UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(User, UserAdmin)
