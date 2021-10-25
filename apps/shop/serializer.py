from rest_framework import serializers
from apps.shop.models import Product, Order, OrderDetail, Payment, PaymentOrder, Shipment


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'active', 'price')
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'client', 'name_client', 'number', 'status', 'date','price')
        read_only_fields = ('id',)


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('id', 'order', 'order_number', 'product', 'product_name', 'quantity', 'value')
        read_only_fields = ('id',)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'number', 'date', 'status', 'date_confirm', 'type', 'value', 'provider')
        read_only_fields = ('id',)


class PaymentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOrder
        fields = ('id', 'order', 'order_number', 'payment', 'payment_number', 'value')
        read_only_fields = ('id',)


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = (
        'id', 'order', 'number_order', 'number', 'date', 'status', 'received', 'date_received', 'name_received',
        'mobile_phone_received', 'direction_received', 'city_received', 'postal_code_received')
        read_only_fields = ('id',)

