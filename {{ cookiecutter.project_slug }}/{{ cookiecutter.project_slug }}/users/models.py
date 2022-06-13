import uuid
from django.contrib.auth.models import (
    BaseUserManager,
)
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from easy_thumbnails.files import get_thumbnailer
from simple_history.models import HistoricalRecords
from easy_thumbnails.fields import ThumbnailerImageField
from unique_upload import unique_upload


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields["role"] = User.ADMIN
        extra_fields["activated_at"] = timezone.now()
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True
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
    new_email = models.EmailField(null=True, default=None)
    role = models.CharField(choices=USER_CHOICES, default=USER, max_length=6)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    username = None
    profile_picture = ThumbnailerImageField(
        upload_to=unique_upload, null=True, blank=True
    )
    activated_at = models.DateTimeField(null=True, blank=True, default=None)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()
    history = HistoricalRecords(excluded_fields=['password'])

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["email"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["first_name"]),
            models.Index(fields=["last_name"]),
            models.Index(fields=["role"]),
        ]

    def activate(self):
        self.activated_at = timezone.now()
        self.is_active = True
        self.save()

    def can_access_role(self, role):
        if self.role == User.ADMIN:
            return True

        if self.role == User.USER:
            return role == User.USER or role == User.EDITOR

        if self.role == User.EDITOR:
            return role == User.EDITOR

        return False

    def delete_profile_picture(self, save):
        if self.profile_picture:
            thumbnailer = get_thumbnailer(self.profile_picture)
            thumbnailer.delete(save=save)
