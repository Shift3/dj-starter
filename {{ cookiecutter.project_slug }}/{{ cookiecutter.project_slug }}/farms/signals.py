from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords

from {{cookiecutter.project_slug}}.notification_system.models import Notification
from {{cookiecutter.project_slug}}.users.models import User

from .models import Farm
from .notifications import FarmCreatedNotification


{%- if cookiecutter.include_notifications == "yes" %}


def send_farm_creation_notification(sender, instance=None, created=False, **kwargs):
    if created:
        Notification.send(
            FarmCreatedNotification(
                {
                    "farm_id": instance.pk,
                    "user_id": str(instance.history.first().history_user_id),
                }
            ),
            User.objects.filter(role=User.ADMIN).exclude(id=instance.history.first().history_user_id)
        )


post_save.connect(
    send_farm_creation_notification,
    sender=Farm,
    dispatch_uid="send_farm_creation_notification"
)
{%- endif % }
