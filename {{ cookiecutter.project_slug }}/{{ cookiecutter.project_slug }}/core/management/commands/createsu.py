from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser based on the information in settings.SEEDED_USER_EMAIL"

    def handle(self, *args, **kwargs):
        email = getattr(settings, "SEEDED_USER_EMAIL", None)
        if email:
            if not User.objects.filter(email=email).exists():
                User.objects.create_superuser(
                    email, User.objects.make_random_password()
                )
                print("Initial user created, reset the password to activate it!")
