{%- if cookiecutter.include_notifications == "yes" %}
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords

from {{ cookiecutter.project_slug }}.notification_system.models import Notification
from {{ cookiecutter.project_slug }}.users.models import User

from .models import Agent
from .notifications import AgentCreatedNotification


def send_agent_creation_notification(sender, instance=None, created=False, **kwargs):
    if created:
        Notification.send(
            AgentCreatedNotification(
                {
                    "agent_id": instance.pk,
                    "user_id": str(instance.history.first().history_user_id),
                }
            ),
            User.objects.filter(role=User.ADMIN).exclude(id=instance.history.first().history_user_id)
        )

post_save.connect(
    send_agent_creation_notification,
    sender=Agent,
    dispatch_uid="send_agent_creation_notification"
)
{%- endif %}
