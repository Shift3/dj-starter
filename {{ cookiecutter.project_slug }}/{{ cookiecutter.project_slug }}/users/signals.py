from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from djoser.signals import user_activated
from rest_framework.authtoken.models import Token


@receiver(user_activated)
def save_activation_date(sender, user, request, **kwargs):
    if user.activated_at is None:
        user.activate()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
