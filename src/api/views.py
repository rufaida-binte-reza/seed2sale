# api/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from pathlib import Path
from products.models import Category, Product, Wishlist, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    WishlistSerializer,
)

# ---------- ViewSets ----------
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class WishlistViewSet(ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

# ---------- JWT helper ----------
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': getattr(user, 'email', None),
            'full_name': getattr(user, 'full_name', None),
        })


class FrontendPageView(APIView):
    """
    Serve static frontend HTML pages during development
    The view loads the file from repo-root/frontend/<page>.html
    """
    permission_classes = []

    def get(self, request, page: str = 'home'):
        base = Path(settings.BASE_DIR).parent
        frontend_dir = base / 'frontend'
        page_path = frontend_dir / f"{page}.html"
        if not page_path.exists():
            return HttpResponseNotFound('Page not found')
        content = page_path.read_text(encoding='utf-8')
        return HttpResponse(content, content_type='text/html')