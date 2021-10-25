from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from apps.user.models import User
from omni.general_class import ManagerAccount
from omni.tasks import send_email



@receiver(post_save,sender=User)
def send_email_confirm(sender, instance=User, created=False, **kwargs):
    if created:
        token_generator = PasswordResetTokenGenerator()
        token=token_generator.make_token(instance)
        subject = 'Confirm your email'
        template = 'registration/email_confirm_welcome.html'
        recipients = instance.email
        url = ManagerAccount.get_url_account_activate(instance,token)
        context = {'name':f'{instance.first_name} {instance.last_name}', 'url':url}
        send_email.delay(subject,[recipients],html_template=template, context=context)


