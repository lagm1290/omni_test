from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from omni.general_class import RegexValidatorCommon

# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, date_joined=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        _('Email'), max_length=100, db_column='email',unique=True, help_text=_('Email')
    )
    password = models.CharField(_('password'), max_length=128)
    slug = models.SlugField(max_length=500, blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    identity = models.CharField(
        _('Identity'), max_length=20, db_column='identity', help_text=_('Identity')
    )
    first_name = models.CharField(
        _('First Name'), max_length=100, db_column='first_name', help_text=_('First Name')
    )
    last_name = models.CharField(
        _('Last Name'), max_length=100, db_column='last_name', help_text=_('Last Name')
    )
    mobile_phone = models.CharField(
        _('Mobile Phone'), db_column='mobile_phone', blank=True,null=True,max_length=10, help_text=_('Mobile Phone'),
        validators=[RegexValidatorCommon.phone()]
    )
    direction = models.CharField(
        _('Direction'), max_length=250,blank=True, null=True, db_column='direction',help_text=_('Direction')
    )
    city = models.CharField(
        _('City'), max_length=50,blank=True, null=True, db_column='city', help_text=_('City')
    )
    postal_code = models.CharField(
        _('Postal Code'), max_length=20,blank=True, null=True, db_column='postal_code', help_text=_('Postal Code')
    )

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return  f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return f'{self.first_name} {self.last_name}'.strip()


    class Meta:
        app_label = 'user'
        db_table = 'user_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

class OmniPermissions(models.Model):
    class Meta:
        app_label = 'user'
        managed = False  # No database management for this model
        # Add here all the application permissions
        permissions = (
            ('client', 'Client'),
            ('admin', 'Admin'),
        )