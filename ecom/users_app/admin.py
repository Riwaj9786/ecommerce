from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from users_app import models
from django.contrib.admin import ModelAdmin

class UserAdmin(ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser', 'created_at')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    fields = ('email', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'groups', 'user_permissions')
    search_fields = ['email']
    readonly_fields = ['last_login']

admin.site.register(models.AppUser, UserAdmin)

class ProfileAdmin(ModelAdmin):
    list_display = ('user_link','display_profile_picture',  'first_name_link', 'last_name_link', 'phone_link')
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ('email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'profile_picture', 'user', 'academic_background', 'bio', 'address_line1', 'created_at', 'updated_at', 'created_by')

    def display_profile_picture(self, obj):
        """Display profile picture as a thumbnail in the admin list."""
        if obj.profile_picture:
            return format_html('<img src="{}" style="border-radius: 50%; width: 50px; height: 50px;" />', obj.profile_picture.url)
        return "No image"
    
    display_profile_picture.short_description = 'Profile Picture'

    def user_link(self, obj):
        """Make the user column clickable and link to the edit page."""
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user)

    def first_name_link(self, obj):
        """Make the user column clickable and link to the edit page."""
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.first_name)
    
    def last_name_link(self, obj):
        """Make the user column clickable and link to the edit page."""
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.last_name)
    
    def phone_link(self, obj):
        """Make the user column clickable and link to the edit page."""
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html('<a href="{}"><p>{}</p></a>', url, obj.phone)
 
    user_link.short_description = 'User'
    first_name_link.short_description = 'First Name'
    last_name_link.short_description = 'Last Name'
    phone_link.short_description = 'Phone'

admin.site.register(models.Profile, ProfileAdmin)