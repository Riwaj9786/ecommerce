from rest_framework import serializers
from ecommerce_app.models import (
    Product,
    ProductImage
)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'category', 'stock', 'product_images')