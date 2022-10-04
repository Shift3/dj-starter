import dramatiq

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from twilio.rest import Client


@dramatiq.actor
def send_email_later(serialized_email):
    msg = EmailMultiAlternatives(
        serialized_email["subject"],
        serialized_email["body"],
        serialized_email["from_email"],
        serialized_email["to"],
    )
    msg.cc = serialized_email["cc"]

    for content, mimetype in serialized_email["alternatives"]:
        msg.attach_alternative(content, mimetype)

    msg.send()

@dramatiq.actor
def send_text_later(to_number, message):
    if settings.DEBUG:
        print("Sending text message:")
        print(f"From:    {settings.TWILIO_FROM_NUMBER}")
        print(f"To:      {to_number}")
        print(f"Message: {message}")
    else:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            to=to_number,
            from_=settings.TWILIO_FROM_NUMBER,
            body=message
        )
