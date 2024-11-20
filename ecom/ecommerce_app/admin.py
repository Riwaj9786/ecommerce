from django.contrib import admin
from ecommerce_app import models
from django.contrib.admin import ModelAdmin

# Register your models here.
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category', 'supplier']

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category)
