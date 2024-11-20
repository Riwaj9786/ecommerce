from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    CreateAPIView
)

from django.shortcuts import get_object_or_404

from ecommerce_app.serializers import (
    ProductImageSerializer,
    ProductSerializer,
)
from ecommerce_app.models import (
    ProductImage,
    Product
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
)

# Create your views here.
class ProductAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
      
        
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(supplier=request.user)
            return Response({
                'product': serializer.data,
                'message': "Product Added Successfully"
            }, 
            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
