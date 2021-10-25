from django.dispatch import receiver
from django.db.models.signals import post_save , post_delete
from apps.shop.models import Order , PaymentOrder, Shipment
from omni.tasks import send_email

@receiver(post_save,sender=PaymentOrder)
def change_status_order_paid(instance=PaymentOrder, created= False, **kwargs):
    if created:
        Order.objects.filter(id=instance.order.pk).update(status=Order.PAID)

@receiver(post_delete, sender=PaymentOrder)
def change_status_order_delete(sender, instance, *args, **kwargs):
    Order.objects.filter(id=instance.order.pk).update(status=Order.CREATED)


@receiver(post_save,sender=Shipment)
def change_status_order_send(instance=Shipment, created=False, **kwargs):
    if not created:
        recipients = instance.order.client.email
        if instance.status == Shipment.Status.SEND:
            # Change order
            Order.objects.filter(id=instance.order.pk).update(status=Order.SEND)
            subject = f'Order Nª {instance.order.number} {instance.order.status}'
            template = 'shop/order_send.html'

            context = {'context':{"shipment": instance.number,
                       "order":instance.order.number,
                       "date_send":instance.date_send,
                       "name_received":instance.name_received,
                       "date_received":instance.date_received,
                       "mobile_phone_received":instance.mobile_phone_received,
                       "direction_received":instance.direction_received,
                       "city_received":instance.city_received,
                       "postal_code_received":instance.postal_code_received
                       }}
        elif instance.status == Shipment.Status.RECEIVED:
            subject = f'Order Nª {instance.order.number} received'
            template = 'shop/order_received.html'
            context = {'context':{"shipment": instance.number,
                       "date_received":instance.date_received
                       }}
        send_email.delay(subject, [recipients],html_template=template, context=context)

@receiver(post_delete, sender=Shipment)
def change_status_order_send_delete(instance=Shipment, **kwargs):
    Order.objects.filter(id=instance.order.pk).update(status=Order.PAID)

