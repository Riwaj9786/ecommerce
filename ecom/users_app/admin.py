from django.utils.html import format_html
from django.contrib import admin
from users_app import models
from django.contrib.admin import ModelAdmin

@admin.register(models.AppUser)
class UserAdmin(ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    fields = ('email', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'groups', 'user_permissions')
    search_fields = ['email']
    readonly_fields = ['last_login']


@admin.register(models.Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('user','display_profile_picture', 'first_name', 'last_name', 'phone', 'created_at')
    list_display_links = ('user', 'first_name', 'last_name', 'phone')
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ('email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'profile_picture', 'user', 'academic_background', 'bio', 'address_line1', 'created_at', 'updated_at', 'created_by')

    def display_profile_picture(self, obj):
        """Display profile picture as a thumbnail in the admin list."""
        if obj.profile_picture:
            return format_html('<img src="{}" style="border-radius: 50%; width: 50px; height: 50px;" />', obj.profile_picture.url)
        return "No image"
    
    display_profile_picture.short_description = 'Profile Picture'