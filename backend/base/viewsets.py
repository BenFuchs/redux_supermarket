# viewsets.py
from rest_framework import viewsets
from .models import  Product, Cart
from .serializers import  ProductSerializer, CartSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# class CartViewSet(viewsets.ModelViewSet):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer