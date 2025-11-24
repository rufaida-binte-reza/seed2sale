from rest_framework import serializers
from .models import Warehouse, Inventory

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')
    class Meta:
        model = Inventory
        fields = ['id','warehouse','warehouse_name','product','product_name','quantity','batch_code','last_updated']
