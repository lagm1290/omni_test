from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class RegexValidatorCommon(object):
    @staticmethod
    def phone():
        return RegexValidator(r'^[\+]?[0-9]+$', _('only characters, 0-9'))


class ManagerAccount(object):
    @staticmethod
    def get_url_account_activate(user, token):
        domain = Site.objects.get(name='frontend_account')
        url = "http://{}/{}/{}".format(domain, urlsafe_base64_encode(force_bytes(user.pk)), token)
        return url


class General(object):
    @staticmethod
    def get_code_number(ind='x'):
        number = 100
        return format(id(number), ind)


