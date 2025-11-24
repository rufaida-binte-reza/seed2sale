# from django.shortcuts import render

# from rest_framework import viewsets
# from .models import Product, Category
# from .serializers import ProductSerializer, CategorySerializer
# from rest_framework.permissions import IsAuthenticatedOrReadOnly

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all().order_by('-created_at')
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

from rest_framework import viewsets, permissions, filters
from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, WishlistSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category','farmer').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name','description','farmer__full_name','category__name']
    ordering_fields = ['price','created_at','stock']

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()  
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

