import logging

from {{ cookiecutter.project_slug }}.core.tasks import send_email_later

from .models import DatabaseNotification


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

            serialized_email = dict(
                to=[user.email],
                cc=email.cc,
                from_email=email.from_email,
                subject=email.subject,
                body=email.body,
                attachments=email.attachments,
                extra_header=email.extra_headers,
                alternatives=email.alternatives,
            )

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
            sms = notification.as_sms(user)
            print(sms)
        else:
            logger = logging.getLogger()
            logger.error(
                "'%s' cannot send sms, as it does not define a 'as_sms' method",
                notification.__class__.__name__,
            )
