from django.contrib import admin
from apps.user.models import User
from django.contrib import admin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, UserChangeForm, UserCreationForm
)



csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    list_display = (
        'identity', 'first_name', 'last_name', 'email', 'mobile_phone', 'direction', 'city',
        'postal_code'
    )

    list_display_links = ('identity',)

    search_fields = (
        'identity', 'email', 'first_name', 'last_name'
    )
    filter_horizontal = ('groups', 'user_permissions',)
