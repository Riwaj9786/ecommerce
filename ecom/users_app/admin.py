from django.contrib import admin
from users_app import models
from django.contrib.admin import ModelAdmin

class UserAdmin(ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')

admin.site.register(models.AppUser, UserAdmin)