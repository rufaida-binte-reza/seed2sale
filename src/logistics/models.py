from django.db import models
from django.conf import settings
from orders.models import Order

class DriverProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')
    phone = models.CharField(max_length=32, blank=True)
    vehicle = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.full_name}'

class DeliveryJob(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='delivery_jobs')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    status = models.CharField(max_length=30, default='assigned')
    eta = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Job {self.id} - Order {self.order.id}'
