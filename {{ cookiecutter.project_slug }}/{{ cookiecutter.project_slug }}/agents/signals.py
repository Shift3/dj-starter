{%- if cookiecutter.include_notifications == "yes" %}
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from simple_history.models import HistoricalRecords

from {{ cookiecutter.project_slug }}.notification_system.models import Notification
from {{ cookiecutter.project_slug }}.users.models import User

from .models import Agent
from .notifications import AgentCreatedNotification


@receiver(post_save, sender=Agent)
def send_agent_creation_notification(sender, instance=None, created=False, **kwargs):
    if created:
        Notification.send(
            AgentCreatedNotification(
                {
                    "agent_id": instance.pk,
                    "user_id": str(HistoricalRecords.context.request.user.id),
                }
            ),
            User.objects.filter(role=User.ADMIN).exclude(id=HistoricalRecords.context.request.user.id)
        )
{%- endif %}
