from django.apps import AppConfig


class NotificationSystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{{ cookiecutter.project_slug }}.notification_system"
