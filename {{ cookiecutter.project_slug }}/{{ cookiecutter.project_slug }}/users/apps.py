from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{{ cookiecutter.project_slug }}.users"

    def ready(self):
        import {{ cookiecutter.project_slug }}.users.signals
