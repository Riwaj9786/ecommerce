from rest_framework import serializers
from ecommerce_app.models import (
    Cart,
    CartItem,
    Category,
    Product,
    ProductImage
)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'product')
        read_only_fields = ('product',)


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('product_id', 'name', 'description', 'price', 'category', 'stock', 'product_images', 'supplier')
        read_only_fields = ('product_id', 'supplier')


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('cart', 'product', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(source='cart_item', many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ('cart_id', 'user', 'total_amount', 'is_checked_out', 'cart_items',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description')
        read_only_fields = ('category_id',)