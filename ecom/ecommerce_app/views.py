from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    DestroyAPIView,
)

from django.shortcuts import get_object_or_404
from users_app.models import AppUser
from ecommerce_app.permissions import IsOwner, IsOwnerSafe
from ecommerce_app.serializers import (
    CartItemSerializer,
    CartSerializer,
    ProductImageSerializer,
    ProductSerializer,
)
from ecommerce_app.models import (
    ProductImage,
    Product,
    Cart,
    CartItem
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class ProductAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name',)
    filterset_fields = ('category', 'supplier',)


    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(supplier=request.user)
            return Response(
                {
                    'product': serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDestroyAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsOwner,)

# class ProductAPIView(APIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)

#     def get(self, request, pk=None):
#         if pk:
#             product = get_object_or_404(Product, pk=pk)
#             serializer = ProductSerializer(product)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             product = Product.objects.all()
#             serializer = ProductSerializer(product, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
      
        
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(supplier=request.user)
#             return Response({
#                 'product': serializer.data,
#                 'message': "Product Added Successfully"
#             }, 
#             status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImageAPIView(ListCreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = (IsOwnerSafe,)

    def list(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        images = ProductImage.objects.filter(product=product)

        serializer = ProductImageSerializer(images, many=True)
        return Response(
            {'images': serializer.data},
            status=status.HTTP_200_OK
        )            
    
    def create(self, request, pk,  *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {'message': 'Product Doesn\'t Exist!'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(
                {
                    'message': 'Image Added Successfully!',
                    'image': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': 'you are here', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        

class CartAPIView(APIView):
    permission_classes = (IsOwner,)

    def get(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user)

        if cart.exists():
            serializer = CartSerializer(cart, many=True)

            return Response(
                serializer.data,
                status= status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': "There is no Cart Item for this user!"},
                status= status.HTTP_404_NOT_FOUND
            )


class CategoryAPIView(APIView):
    pass


class AddToCartAPIView(APIView):
    pass