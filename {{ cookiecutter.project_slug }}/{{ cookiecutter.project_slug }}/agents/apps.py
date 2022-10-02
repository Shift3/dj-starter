from django.apps import AppConfig
import os


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{{ cookiecutter.project_slug }}.agents"

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from .signals import send_agent_creation_notification
            from .models import Agent
            from django.db.models.signals import post_save

            post_save.connect(
                send_agent_creation_notification,
                sender=Agent,
                dispatch_uid="send_agent_creation_notification"
            )
