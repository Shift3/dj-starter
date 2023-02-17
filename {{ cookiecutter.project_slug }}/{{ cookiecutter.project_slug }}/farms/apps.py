from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dj_starter_demo.farms"

    def ready(self):
        from . import signals
