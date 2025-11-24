from django.db import models
from orders.models import Order
from django.conf import settings

class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cod", "Cash on Delivery"),
        ("card", "Card Payment"),
        ("bkash", "Bkash"),
        ("nagad", "Nagad"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"
