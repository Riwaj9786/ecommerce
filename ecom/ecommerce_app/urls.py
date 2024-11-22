from django.urls import path, include
from ecommerce_app import views
from rest_framework import routers

urlpatterns = [
    path('products/', views.ProductAPIView.as_view(), name='products'),
    path('products/images/<pk>/', views.ProductImageAPIView.as_view(), name='product_images'),
    path('carts/', views.CartAPIView.as_view(), name='cart-view'),
    path('products/delete/<pk>/', views.ProductDestroyAPIView.as_view(), name='product-delete'),
    path('category/', views.CategoryAPIView.as_view(), name='category'),
    # path('product/<product_pk>/add_to_cart/<cart_pk>/', views.AddToCartAPIView.as_view(), name='add-to-cart'),
]