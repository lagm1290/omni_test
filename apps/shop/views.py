import datetime

from django.shortcuts import render
from django.db.models import Q, F
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from functools import reduce
import django_excel as excel
import operator

from apps.shop.models import Product, Order, OrderDetail, Payment, PaymentOrder, Shipment
from apps.shop.serializer import (ProductSerializer, OrderSerializer, OrderDetailSerializer, PaymentSerializer,
                                  PaymentOrderSerializer, ShipmentSerializer)
from apps.user.permissions import ClientPermission
from omni.general_class import General
from apps.shop.raw_query import ShopQueries


@permission_classes([IsAuthenticated])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ClientPermission]

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(ProductViewSet, self).update(request, *args, **kwargs)

    def get_queryset(self):
        list_q = self.request.GET.get('query', '')
        get_is_active = self.request.GET.get('is_active', None)
        queryset = self.queryset

        if get_is_active:
            queryset = queryset.filter(active=False)

        fields_look = [
            'name__icontains'
        ]
        for query_term in list_q:
            on_queries = [Q(**{field_look: query_term})
                          for field_look in fields_look]
            queryset = queryset.filter(reduce(operator.or_, on_queries))

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "element deleted"}, status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('client').all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(number=General.get_code_number('o'), client=self.request.user, status=Order.CREATED)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(OrderViewSet, self).update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        list_q = self.request.GET.get('query', '')

        fields_look = [
            'number__contains'
        ]

        for query_term in list_q:
            on_queries = [Q(**{field_look: query_term})
                          for field_look in fields_look]
            queryset = queryset.filter(reduce(operator.or_, on_queries))

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.status == Order.CREATED:
            raise ValidationError(detail='it is not possible to delete the element, because the order is in process.')
        self.perform_destroy(instance)
        return Response({"message": "order deleted"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='report')
    def report(self, request):
        get_type = request.data.get('type', None)
        if get_type not in ['paid', 'send']:
            raise ValidationError(detail='the type is incorrect')

        if get_type == 'paid':
            query = ShopQueries.product_payment(status=Payment.Status.APPROVED)
            export = []
            for result in query:
                export.append([
                    result.order,
                    result.payment,
                    result.value,
                    result.date_confirm
                ])
            headers = ['ORDER', 'PAYMENT', 'VALUE', 'DATE']

        elif get_type == 'send':
            query = ShopQueries.product_send(status=Shipment.Status.ALL_ACTION)
            export = []
            for result in query:
                export.append([
                    result.order,
                    result.shipment,
                    result.name,
                    result.date,
                    result.mobile_phone,
                    result.direction,
                    result.city,
                    result.postal_code
                ])

            headers = ['ORDER', 'SHIPMENT', 'NAME', 'DATE', 'MOBILE PHONE', 'DIRECTION', 'CITY', 'POSTAL CODE']

        export.insert(0, headers)
        if len(export) > 1:
            sheet = excel.pe.Sheet(export)
            return excel.make_response(sheet,"csv", file_name='list_order_paid.csv')
        else:
            return Response(
                {"message": "Sorry, no records were found"},
                status=status.HTTP_200_OK
            )


@permission_classes([IsAuthenticated])
class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.select_related('order', 'product').all()
    serializer_class = OrderDetailSerializer

    def perform_create(self, serializer):
        get_quantity = serializer.validated_data['quantity']
        get_product = serializer.validated_data['product']
        get_order = serializer.validated_data['order']

        if get_quantity == 0:
            raise ValidationError(detail='The Quantity Must Be Greater Than 0')

        get_order_detail = OrderDetail.objects.filter(order=get_order, product=get_product).first()
        if get_order_detail:
            get_order_detail.quantity = F('quantity') + get_quantity
            get_order_detail.save()
            return Response(get_order_detail)
        get_val = get_quantity * get_product.price
        serializer.save(value=get_val)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(OrderDetailViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.order.status == Order.CREATED:
            raise ValidationError(detail='it is not possible to delete the element, because the order is in process.')
        self.perform_destroy(instance)
        return Response({"message": "element deleted"}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        list_q = self.request.GET.get('query', '')
        get_order = self.request.GET.get('order')
        queryset = self.queryset

        if get_order:
            queryset = queryset.filter(order=get_order)

        fields_look = [
            'order__number__contains',
            'product__name__contains'
        ]
        for query_term in list_q:
            on_queries = [Q(**{field_look: query_term})
                          for field_look in fields_look]
            queryset = queryset.filter(reduce(operator.or_, on_queries))

        return queryset


@permission_classes([IsAuthenticated])
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        get_type = serializer.validated_data['type']
        if get_type not in Payment.Types.ALL:
            raise ValidationError(detail='The Type Must Be Debit or Credit')

        serializer.save(number=General.get_code_number(),
                        status=Payment.Status.PENDING,
                        client=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        get_type = request.data.get('type')
        if Payment.objects.filter(id=kwargs['pk'], status=Payment.Status.APPROVED).exists():
            raise ValidationError(detail='The Object Cannot Be Updated')

        if get_type not in Payment.Types.ALL:
            raise ValidationError(detail='The Type Must Be Debit or Credit')
        return super(PaymentViewSet, self).update(request, *args, **kwargs)

    def get_queryset(self):
        list_q = self.request.GET.get('query', '')
        queryset = self.queryset

        fields_look = [
            'number__icontains',
        ]
        for query_term in list_q:
            on_queries = [Q(**{field_look: query_term})
                          for field_look in fields_look]
            queryset = queryset.filter(reduce(operator.or_, on_queries))

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.status == Payment.Status.PENDING:
            raise ValidationError(detail='it is not possible to delete the element, because the payment is in process.')
        self.perform_destroy(instance)
        return Response({"message": "payment deleted"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='confirm')
    def check_confirm(self, request):
        get_payment = request.data.get('payment', None)
        get_action = request.data.get('action', None)
        if get_payment and get_action:
            if get_action not in Payment.Status.ALL_CONF:
                raise ValidationError(detail='The Field Action Is Not Correct')
            else:
                Payment.objects.filter(id=get_payment).update(
                    status=get_action,
                    date_confirm=datetime.date.today()
                )
                return Response('The Payment hhs Been Confirmed')
        else:
            raise ValidationError(detail='The Fields payment and action Are Required')


@permission_classes([IsAuthenticated])
class PaymentOrderViewSet(viewsets.ModelViewSet):
    queryset = PaymentOrder.objects.select_related('order', 'payment').all()
    serializer_class = PaymentOrderSerializer

    def perform_create(self, serializer):
        get_order = serializer.validated_data['order']
        get_payment = serializer.validated_data['payment']
        get_value = serializer.validated_data['value']

        if not get_value > 0:
            raise ValidationError(detail='the value must be greater than 0')
        if get_payment.status != Payment.Status.APPROVED:
            raise ValidationError(detail='Error, payment is not approved')
        if get_order.status != Order.CREATED:
            raise ValidationError(detail='Error, the order must be created')
        serializer.save()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        get_order = request.data.get('order', None)
        get_payment = request.data.get('payment', None)
        get_value = request.data.get('value', None)

        if not get_value > 0:
            raise ValidationError(detail='the value must be greater than 0')
        if get_payment.status != Payment.Status.APPROVED:
            raise ValidationError(detail='Error, payment is not approved')
        if get_order.status != Order.CREATED:
            raise ValidationError(detail='Error, the order must be created')

        return super(PaymentOrderViewSet, self).update(request, *args, **kwargs)

    def get_queryset(self):
        list_q = self.request.GET.get('query', '')
        get_payment = self.request.GET.get('payment', None)
        get_order = self.request.GET.get('order', None)
        queryset = self.queryset

        if get_payment:
            queryset = queryset.filter(payment=get_payment)

        if get_order:
            queryset = queryset.filter(order=get_order)

        fields_look = [
            'order__number__icontains',
            'payment__number__icontains'
        ]
        for query_term in list_q:
            on_queries = [Q(**{field_look: query_term})
                          for field_look in fields_look]
            queryset = queryset.filter(reduce(operator.or_, on_queries))

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.order.status == Order.SENT:
            raise ValidationError(detail='it is not possible to delete')
        self.perform_destroy(instance)
        return Response({"message": "the element deleted"}, status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
class ShipmentOrderViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.select_related('order').all()
    serializer_class = ShipmentSerializer

    def perform_create(self, serializer):
        get_order = serializer.validated_data['order']
        if get_order.status != Order.PAID:
            raise ValidationError(detail='The selected order is not in the correct state')
        serializer.save(number=General.get_code_number(), status=Shipment.Status.CREATED)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        get_order = request.data.get('order')
        if get_order.status != Order.PAID:
            raise ValidationError(detail='The selected order is not in the correct state')

        return super(ShipmentOrderViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != Shipment.Status.CREATED:
            raise ValidationError(detail='The shipment cannot be deleted')
        self.perform_destroy(instance)
        return Response({"message": "element deleted"}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        list_q = self.request.GET.get('query', '')
        get_order = self.request.GET.get('order')
        queryset = self.queryset
        if get_order:
            queryset = queryset.filter(order=get_order)

        fields_look = [
            'order__number__icontains',
            'number__icontains'
        ]
        for query_term in list_q:
            on_queries = [Q(**{field_look: query_term})
                          for field_look in fields_look]
            queryset = queryset.filter(reduce(operator.or_, on_queries))

        return queryset

    @action(detail=False, methods=['post'], url_path='action')
    def action(self, request):
        get_shipment = request.data.get('shipment', None)
        get_action = request.data.get('action', None)
        if get_action not in Shipment.Status.ALL_ACTION:
            raise ValidationError(detail='the action is incorrect')

        obj_shipment = Shipment.objects.get(pk=get_shipment)
        obj_shipment.status = get_action
        obj_shipment.date_send = datetime.date.today()
        if get_action == Shipment.Status.RECEIVED:
            obj_shipment.received = True
            obj_shipment.date_received = datetime.date.today()
        obj_shipment.save()
        return Response('The action has been process')
