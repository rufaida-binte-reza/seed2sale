# from rest_framework import serializers
# from .models import Order, OrderItem

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, read_only=True)
#     class Meta:
#         model = Order
#         fields = ['id', 'customer', 'total_price', 'status', 'created_at', 'items']

from rest_framework import serializers
from .models import Order, OrderItem, Payment
from products.serializers import ProductSerializer
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','unit_price','total_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from products.models import Product
        self.fields['product'].queryset = Product.objects.all()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','customer','total_price','status','created_at','notes','items']
        read_only_fields = ['customer','created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(customer=user, **validated_data)
        total = 0
        for it in items_data:
            p = it['product']
            qty = it['quantity']
            unit_price = p.price
            tp = unit_price * qty
            OrderItem.objects.create(order=order, product=p, quantity=qty, unit_price=unit_price, total_price=tp)
            total += tp
            # decrement stock
            if p.stock >= qty:
                p.stock -= qty
                p.save()
        order.total_price = total
        order.save()
        return order
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['order']

