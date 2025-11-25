# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('home.html',                  views.home,                   name='home'),
    path('catalog.html',               views.catalog,                name='catalog'),
    path('product_detail.html',        views.product_detail,         name='product_detail'),
    path('login.html',                 views.login,                  name='login'),
    path('cart_checkout.html',         views.cart_checkout,          name='cart_checkout'),
    path('admin_dashboard.html',       views.admin_dashboard,        name='admin_dashboard'),
    path('customer_dashboard.html',    views.customer_dashboard,     name='customer_dashboard'),
    path('inventory.html',             views.inventory,              name='inventory'),
    path('farmer_profile.html',        views.farmer_profile,         name='farmer_profile'),
    path('driver_jobs.html',           views.driver_jobs,            name='driver_jobs'),
    path('about_contact_faq.html',     views.about_contact_faq,      name='about_contact_faq'),
]