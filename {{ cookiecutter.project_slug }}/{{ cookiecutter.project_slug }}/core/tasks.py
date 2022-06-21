import dramatiq

from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings


@dramatiq.actor
def send_email_later(serialized_email):
    print(settings.EMAIL_BACKEND)
    msg = EmailMultiAlternatives(
        serialized_email["subject"],
        serialized_email["body"],
        serialized_email["from_email"],
        serialized_email["to"],
    )
    for content, mimetype in serialized_email["alternatives"]:
        msg.attach_alternative(content, mimetype)
    msg.send()
