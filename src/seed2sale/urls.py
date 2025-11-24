"""
URL configuration for seed2sale project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.views import CartViewSet, CartItemViewSet
from accounts.views import AddressViewSet, FarmerProfileViewSet
from products.views import WishlistViewSet, ReviewViewSet
from orders.views import PaymentViewSet

router = DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
router.register('cart-items', CartItemViewSet, basename='cartitem')
router.register('addresses', AddressViewSet, basename='address')
router.register('farmer-profile', FarmerProfileViewSet, basename='farmer-profile')
router.register('wishlist', WishlistViewSet, basename='wishlist')
router.register('payment', PaymentViewSet, basename='payment')
router.register(r"reviews", ReviewViewSet, basename="reviews")


# urlpatterns = [
#     path('api/', include(router.urls)),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts endpoints (register + token)
    path('accounts/', include('accounts.urls')),

    # API namespaces
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('warehouse.urls')),
    path('api/', include('logistics.urls')),
    path('api/', include(router.urls)),
    path('api/products/<int:product_id>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("api/accounts/", include("accounts.urls")),

]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


