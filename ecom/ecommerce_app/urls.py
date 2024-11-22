from django.urls import path, include
from ecommerce_app import views
from rest_framework import routers

urlpatterns = [
    path('products/', views.ProductAPIView.as_view(), name='products'),
    path('products/images/<pk>/', views.ProductImageAPIView.as_view(), name='product_images'),
    path('carts/', views.CartAPIView.as_view(), name='cart-view'),
    path('products/<user_id>/', views.UserProductsView.as_view(), name='owner-products'),
    path('category/', views.CategoryAPIView.as_view(), name='category'),
]