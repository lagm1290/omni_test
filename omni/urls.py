"""omni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from apps.user.views import activate_user_account, change_password , AuthToken
from django.urls import include, path, re_path
from apps.user import urls as urls_user
from apps.shop import urls as urls_shop

url_api_rest = [
    path('user/', include(urls_user)),
    path('shop/', include(urls_shop)),
]

urlpatterns = [
    re_path(
        'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate_user_account,
        name='activate'),
    path('changepassword/', change_password, name='change_password'),
    path('admin/', admin.site.urls),
    path('rest/', include(url_api_rest)),
    path('rest/auth/', AuthToken.as_view()),
]
