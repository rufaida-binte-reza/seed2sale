# from rest_framework.routers import DefaultRouter
# from .views import ProductViewSet, CategoryViewSet

# router = DefaultRouter()
# router.register('products', ProductViewSet)
# router.register('categories', CategoryViewSet)

# urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r"reviews", ReviewViewSet, basename="reviews")


urlpatterns = router.urls
