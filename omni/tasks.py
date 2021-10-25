from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
from omni.settings import DEFAULT_FROM_EMAIL

@shared_task()
def send_email(subject,recipient,body=None,txt_template=None,html_template=None,context=None):
    files_ = []
    from_email = DEFAULT_FROM_EMAIL
    if txt_template:
        text_content = render_to_string(txt_template)
    else:
        text_content = body

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient)
    if html_template:
        html_content = render_to_string(html_template, context={'context': ''} if not context else context)
        msg.attach_alternative(html_content, "text/html")

    if files_:
        for file in files_:
            msg.attach_file(file)
    msg.send()