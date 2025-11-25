# from rest_framework import viewsets, permissions
# from .models import Warehouse, Inventory
# from .serializers import WarehouseSerializer, InventorySerializer

# class WarehouseViewSet(viewsets.ModelViewSet):
#     queryset = Warehouse.objects.all()
#     serializer_class = WarehouseSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# class InventoryViewSet(viewsets.ModelViewSet):
#     queryset = Inventory.objects.select_related('warehouse','product').all()
#     serializer_class = InventorySerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def catalog(request):
    return render(request, "catalog.html")

def product_detail(request):
    return render(request, "product_detail.html")

def login_page(request):
    return render(request, "login.html")

def cart_checkout(request):
    return render(request, "cart_checkout.html")

def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

def customer_dashboard(request):
    return render(request, "customer_dashboard.html")

def inventory(request):
    return render(request, "inventory.html")

def farmer_profile(request):
    return render(request, "farmer_profile.html")

def driver_jobs(request):
    return render(request, "driver_jobs.html")

def about_contact_faq(request):
    return render(request, "about_contact_faq.html")

