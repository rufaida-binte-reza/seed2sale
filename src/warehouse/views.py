from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def catalog(request):
    return render(request, 'core/catalog.html')

def product_detail(request):
    return render(request, 'core/product_detail.html')     
 
def login(request):     
    return render(request, 'core/login.html')   

def cart_checkout(request):
    return render(request, 'core/cart_checkout.html')

def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html') 

def customer_dashboard(request):
    return render(request, 'core/customer_dashboard.html')  

def inventory(request):
    return render(request, 'core/inventory.html')   

def farmer_profile(request):
    return render(request, 'core/farmer_profile.html')  

def driver_jobs(request):
    return render(request, 'core/driver_jobs.html') 

def about_contact_faq(request):
    return render(request, 'core/about_contact_faq.html')

from django.conf import settings
from django.shortcuts import render             