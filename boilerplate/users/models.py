import uuid
from django.contrib.auth.models import (
    BaseUserManager,
)
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from djoser.signals import user_activated
from rest_framework.authtoken.models import Token
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['role'] = User.ADMIN
        extra_fields['activated_at'] = timezone.now()
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    USER = "USER"
    EDITOR = "EDITOR"
    ADMIN = "ADMIN"
    USER_CHOICES = (
        (USER, "user"),
        (EDITOR, "editor"),
        (ADMIN, "admin"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=USER_CHOICES, default=USER, max_length=6)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    username = None
    profile_picture = models.ImageField(
        upload_to="uploads/profile-pictures/", null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True, default=None)

    objects = UserManager()
    history = HistoricalRecords()

    def activate(self):
        self.activated_at = timezone.now()
        self.is_active = True
        self.save()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
            models.Index(fields=['role']),
        ]


@receiver(user_activated)
def save_activation_date(sender, user, request, **kwargs):
    if user.activated_at is None:
        user.activate()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
