import logging

from {{ cookiecutter.project_slug }}.core.tasks import send_email_later, send_text_later
from {{ cookiecutter.project_slug }}.core.serializers import serialize_email

from .serializers import NotificationSerializer
from .models import DatabaseNotification
from django_eventstream import send_event

def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])


class DatabaseBackend:
    def send(self, user, notification):
        if hasattr(notification, "as_database") and callable(notification.as_database):
            data = notification.as_database(user)
            dbnotification = DatabaseNotification.objects.create(
                type=notification.__class__.__name__,
                user=user,
                data=data,
            )
            dbnotification.save()

            # send sse notification
            serializer = NotificationSerializer(dbnotification)
            modified_data = {}
            modified_data.update(serializer.data)
            modified_data['data'] = {}
            for k, v in serializer.data['data'].items():
                modified_data['data'][to_camel_case(k)] = v
            send_event(str(user.id), 'message', modified_data)
        else:
            logger = logging.getLogger()
            logger.error(
                "'%s' cannot send email, as it does not define a 'as_database' method",
                notification.__class__.__name__,
            )


class EmailBackend:
    def send(self, user, notification):
        if hasattr(notification, "as_email") and callable(notification.as_email):
            email = notification.as_email(user)
            email.render()

            serialized_email = serialize_email(email, [user.email])
            send_email_later.send(serialized_email)
        else:
            logger = logging.getLogger()
            logger.error(
                "'%s' cannot send email, as it does not define a 'as_email' method",
                notification.__class__.__name__,
            )


class SMSBackend:
    def send(self, user, notification):
        if hasattr(notification, "as_sms") and callable(notification.as_sms):
            if user.phone_number is not None:
                sms = notification.as_sms(user)
                send_text_later.send(user.phone_number.as_e164, sms)
        else:
            logger = logging.getLogger()
            logger.error(
                "'%s' cannot send sms, as it does not define a 'as_sms' method",
                notification.__class__.__name__,
            )
