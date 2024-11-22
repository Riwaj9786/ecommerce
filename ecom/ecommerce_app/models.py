import os
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from users_app.models import AppUser

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
    

class Cart(models.Model):
    cart_id = models.CharField(
        primary_key=True,
        max_length=15,
        editable=False
    )

    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='cart')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_checked_out = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.cart_id:
            try:
                last_card = Cart.objects.latest('cart_id')
                last_card_id = last_card.cart_id
                card_number = last_card_id.split('_')[-1]

                new_id = int(card_number) + 1
                self.cart_id = f"CART_{new_id:04d}"
            
            except Cart.DoesNotExist:
                self.cart_id = "CART_0001"

        self.total_amount = self.calculate_total_amount()

        super().save(*args, **kwargs)

    def calculate_total_amount(self):
        total = sum(item.product.price * item.quantity for item in self.cart_item.all())
        return total

    def __str__(self):
        return f"{self.cart_id}-{self.user}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        original_quantity = 0

        if self.pk:
            cart_item = CartItem.objects.get(pk=self.pk)
            original_quantity = cart_item.quantity

        quantity_difference = self.quantity-original_quantity

        if self.product.stock < quantity_difference:
            raise ValidationError("Your order quantity is more than the current stock!")
        else:
            self.product.stock -= quantity_difference

        self.product.save()
        super().save(*args, **kwargs)
        self.cart.save()


    def delete(self, *args, **kwargs):
        self.product.stock+=self.quantity
        self.product.save()

        super().delete(*args, **kwargs)
        self.cart.save()


    def __str__(self):
        return f"Cart Item - {self.product.name} in {self.cart.cart_id}"