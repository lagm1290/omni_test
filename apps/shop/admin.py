from django.contrib import admin
from apps.shop.models import Product, Order, OrderDetail, Shipment, Payment, PaymentOrder


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'active', 'price'
    )
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'client', 'number', 'status', 'date'
    )
    list_display_links = ('number',)
    search_fields = ('number',)


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = (
        'order','product','quantity', 'value'
    )
    list_display_links = ('order',)
    search_fields = ('order__number','product__name')

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        'order','number','date','status','received','name_received','date_received','date_send',
        'mobile_phone_received','direction_received','city_received','postal_code_received'
    )
    list_display_links = ('number',)
    search_fields = ('number',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'client','number','date','status','date_confirm','type','value','provider'
    )
    list_display_links = ('number',)
    search_fields = ('number',)

@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order','payment','value'
    )
    list_display_links = ('order',)
    search_fields = ('order',)
