# from rest_framework.routers import DefaultRouter
# from .views import WarehouseViewSet, InventoryViewSet

# router = DefaultRouter()
# router.register('warehouses', WarehouseViewSet)
# router.register('inventory', InventoryViewSet)

# urlpatterns = router.urls


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # root → home

    path('catalog/', views.catalog, name='catalog'),
    path('product-detail/', views.product_detail, name='product_detail'),
    path('login/', views.login_page, name='login'),
    path('cart-checkout/', views.cart_checkout, name='cart_checkout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('inventory/', views.inventory, name='inventory'),
    path('farmer-profile/', views.farmer_profile, name='farmer_profile'),
    path('driver-jobs/', views.driver_jobs, name='driver_jobs'),
    path('about-contact-faq/', views.about_contact_faq, name='about_contact_faq'),
]

