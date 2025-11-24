from django.db import models
from django.conf import settings
from products.models import Product

class Warehouse(models.Model):
    name = models.CharField(max_length=200)
    location = models.TextField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Inventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.PositiveIntegerField(default=0)
    batch_code = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('warehouse','product','batch_code')

    def __str__(self):
        return f'{self.product.name} @ {self.warehouse.name}'
