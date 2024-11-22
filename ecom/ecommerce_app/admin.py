from django.contrib import admin
from ecommerce_app import models
from django.contrib.admin import ModelAdmin

# Register your models here.
@admin.register(models.Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category', 'supplier']

admin.site.register(models.ProductImage)
admin.site.register(models.Category)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)