import os
import uuid
from django.db import models

# Create your models here.
def product_image_upload_to(instance, filename):
    # Get the product's ID (or any unique identifier)
    product_id = instance.product.product_id
    # Set the folder path where images will be saved
    return os.path.join('static/product_images', f'product_{product_id}', filename)


class Category(models.Model):
    category_id = models.CharField(
        max_length=12,
        primary_key=True,
        editable=False
    )
    name = models.CharField(
        max_length=30,
        unique=True
    )
    description = models.TextField(
        null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.category_id:
            name = self.name[:3].upper()
            self.category_id = f"{name}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category_id}-{self.name}"
    


class Product(models.Model):
    product_id = models.UUIDField(
        primary_key=True,
        default = uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=40
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category', null=True, blank=True)
    supplier = models.ForeignKey('users_app.AppUser', on_delete=models.CASCADE, related_name='product_supplier')

    def __str__(self):
        return f'{self.name}'
    

class ProductImage(models.Model):   
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_to)
    alt_text = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return f"{self.product.name}-{self.id}"
    