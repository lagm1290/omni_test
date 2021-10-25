from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserConfig(AppConfig):
    name = 'apps.user'
    verbose_name = _('User')

    def ready(self):
        import apps.user.signals



