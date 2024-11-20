from django.urls import path, include
from ecommerce_app import views
from rest_framework import routers

urlpatterns = [
    path('products/', views.ProductAPIView.as_view(), name='products-list'),
    # path('products/create/', views.ProductCreateView.as_view(), name='product-create'),
]