from rest_framework import routers
from apps.shop.views import (ProductViewSet, OrderViewSet, OrderDetailViewSet, PaymentViewSet ,
                             PaymentOrderViewSet,ShipmentOrderViewSet)


router_apirestf = routers.DefaultRouter(trailing_slash=True)
router_apirestf.register(r'product', ProductViewSet)
router_apirestf.register(r'order', OrderViewSet)
router_apirestf.register(r'detail-order', OrderDetailViewSet)
router_apirestf.register(r'payment', PaymentViewSet)
router_apirestf.register(r'order-payment', PaymentOrderViewSet)
router_apirestf.register(r'shipment', ShipmentOrderViewSet)

urlpatterns = router_apirestf.urls
