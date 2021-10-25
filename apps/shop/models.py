from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from apps.user.models import User
from omni.general_class import RegexValidatorCommon



# Create your models here.

class Product(models.Model):
    name = models.CharField(
        _('Name'), db_column='name', max_length=50, help_text=_('Name'), unique=True
    )
    active = models.BooleanField(
        _('Active'), default=True, db_column='is_active', help_text=_('if active = True is shown in the available list')
    )
    price = models.DecimalField(
        _('Price'), db_column='price', default=0.00, decimal_places=3, max_digits=5, help_text=_('Price')
    )


    def __str__(self):
        return self.name

    class Meta:
        app_label = 'shop'
        db_table = 'shop_product'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Order(models.Model):
    CREATED= 'created'
    PAID = 'paid'
    SEND =  'send'

    client = models.ForeignKey(
        User, verbose_name=_('Client'), db_column='client_id', on_delete=models.CASCADE,
        related_name='shop_order', blank=True, null=True, related_query_name='shop_orders', help_text=_('Client')
    )
    number = models.CharField(
        _('Number'), db_column='number', blank=True, null=True, max_length=50, help_text=_('Number'), unique=True
    )
    status = models.CharField(
        _('Status'), db_column='status', blank=True, null=True, max_length=20, help_text=_('Status')
    )
    date = models.DateTimeField(
        _('Date'), auto_now_add=True, db_column='Date', help_text=_('Date Order')
    )


    def __str__(self):
        return self.number

    @property
    def name_client(self):
        return f'{self.client.first_name} {self.client.last_name}'

    @property
    def price(self):
        price_order =  OrderDetail.objects.filter(order=self.pk).aggregate(total = Sum('value'))
        val =0 if not price_order else  price_order.get('total')
        return val

    class Meta:
        app_label = 'shop'
        db_table = 'shop_order'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, verbose_name=_('Order'), db_column='order_id', on_delete=models.CASCADE,
        related_name='shop_order_detail',
        related_query_name='shop_order_details', help_text=_('Order')
    )
    product = models.ForeignKey(
        Product, verbose_name=_('Product'), db_column='product_id', on_delete=models.CASCADE,
        related_name='shop_order_detail',
        related_query_name='shop_order_details', help_text=_('Product')
    )
    quantity = models.PositiveIntegerField(
        _('Quantity'), db_column='quantity', default=1, help_text=_('Quantity')
    )
    value = models.DecimalField(
        _('Value'), db_column='value', default=0.00, decimal_places=2, max_digits=5, help_text=_('Value')
    )

    @property
    def product_name(self):
        return self.product.name

    @property
    def order_number(self):
        return self.order.number

    class Meta:
        app_label = 'shop'
        db_table = 'shop_order_detail'
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'


class Shipment(models.Model):
    class Status:
        CREATED = 'created'
        SEND = 'send'
        RECEIVED = 'received'
        ALL_ACTION = [SEND,RECEIVED]


    order = models.ForeignKey(
        Order, verbose_name=_('Order'), db_column='order_id', on_delete=models.CASCADE, related_name='shop_shipment',
        related_query_name='shop_shipments', help_text=_('Shipment')
    )
    number = models.CharField(
        _('Number'), db_column='number',blank=True, null=True, max_length=50, help_text=_('Number'), unique=True
    )

    date = models.DateTimeField(
        _('Date'), auto_now_add=True, db_column='Date', help_text=_('Date Shipment')
    )
    status = models.CharField(
        _('Status'), db_column='status',blank=True, null=True, max_length=20,help_text=_('Status')
    )
    received = models.BooleanField(
        _('Is Received'), default=False, db_column='is_received', help_text=_('Is Received')
    )
    name_received = models.CharField(
        _('Name Received'), max_length=250, db_column='name_received', help_text=_('Date Received')
    )
    date_received = models.DateField(
        _('Date Received'), db_column='date_received', blank=True, null=True, help_text=_('Date Received')
    )
    date_send = models.DateField(
        _('Date Send'), db_column='date_send',blank=True, null=True, help_text=_('Date Received')
    )
    mobile_phone_received = models.CharField(
        _('Mobile Phone'), db_column='mobile_phone_received', max_length=10, help_text=_('Mobile Phone'),
        validators=[RegexValidatorCommon.phone()]
    )
    direction_received = models.CharField(
        _('Direction'), max_length=250, db_column='direction_received', help_text=_('Direction')
    )
    city_received = models.CharField(
        _('City'), max_length=50, db_column='city_received', help_text=_('City')
    )
    postal_code_received = models.CharField(
        _('Postal Code'), max_length=20, db_column='postal_code_received', help_text=_('Postal Code')
    )

    def __str__(self):
        return self.number

    @property
    def number_order(self):
        return self.order.number

    class Meta:
        app_label = 'shop'
        db_table = 'shop_shipment'
        verbose_name = _('Shipment')
        verbose_name_plural = _('Shipments')


class Payment(models.Model):
    class Types:
        CREDIT = 'credit'
        DEBIT = 'debit'
        ALL = [DEBIT,CREDIT]

    class Status:
        PENDING = 'pending'
        APPROVED = 'approved'
        REJECT = 'reject'
        ALL_CONF = [APPROVED,REJECT]

    client = models.ForeignKey(
        User, verbose_name=_('Client'), db_column='client_id', on_delete=models.CASCADE,
        related_name='shop_payment', related_query_name='shop_payments', help_text=_('Client')
    )

    number = models.CharField(
        _('Number'), db_column='number',blank=True, null=True, max_length=50, help_text=_('Number'), unique=True
    )
    date = models.DateTimeField(
        _('Date'), auto_now_add=True, db_column='Date', help_text=_('Date Payment')
    )
    status = models.CharField(
        _('Status'), db_column='status',blank=True, null=True, max_length=20, help_text=_('Status')
    )
    date_confirm = models.DateField(
        _('Date Confirm'), db_column='date_confirm', help_text=_('Date Confirm'), blank=True, null=True
    )
    type = models.CharField(
        _('Type'), db_column='type', max_length=20, help_text=_('Type')
    )

    value = models.DecimalField(
        _('Value'), db_column='value', default=0.00, decimal_places=2, max_digits=5, help_text=_('Value')
    )

    provider = models.CharField(
        _('Provider'), db_column='provider', max_length=100, help_text=_('Provider')
    )

    def __str__(self):
        return self.number

    class Meta:
        app_label = 'shop'
        db_table = 'shop_payment'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'


class PaymentOrder(models.Model):
    order = models.ForeignKey(
        Order, verbose_name=_('Order'), db_column='order_id', on_delete=models.CASCADE,
        related_name='shop_payment_order',
        related_query_name='shop_payment_orders', help_text=_('Order')
    )
    payment = models.ForeignKey(
        Payment, verbose_name=_('Payment'), db_column='payment_id', on_delete=models.CASCADE,
        related_name='shop_payment_order',
        related_query_name='shop_payment_orders', help_text=_('Payment')
    )
    value = models.DecimalField(
        _('Value'), db_column='value', default=0.00, decimal_places=2, max_digits=5, help_text=_('Value')
    )

    @property
    def order_number(self):
        return self.order.number

    @property
    def payment_number(self):
        return self.payment.number

    class Meta:
        app_label = 'shop'
        db_table = 'shop_payment_order'
        verbose_name = 'Payment Order'
        verbose_name_plural = 'Payment Orders'
