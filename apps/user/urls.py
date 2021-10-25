from rest_framework import routers
from apps.user.views import UserViewSet


router_apirestf = routers.DefaultRouter(trailing_slash=True)
router_apirestf.register(r'user', UserViewSet)
router_apirestf.register(r'auth', UserViewSet)
urlpatterns = router_apirestf.urls
