from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from django_extensions.db.models import TimeStampedModel


class DatabaseNotification(TimeStampedModel, models.Model):
    """DatabaseNotification represents an in-app notification."""
    type = models.CharField(max_length=255)
    data = models.JSONField()
    read = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )

    def mark_read(self):
        if self.read is not None:
            self.read = datetime.now()
            self.save()

    class Meta:
        ordering = ["-created"]


class Notification:
    """This class if for sending notifications. Notifications are sent
    via their associated backends (or the backends you specify when
    calling `Notification.send`)

    Here are some examples of how you would send a notification.

    # Send a notification
    Notification.send(
        SomeNotification(),
        User.objects.filter(id="example")
    )

    # Send a notification via the backends of your choice, instead of
    # the default backends for that notification.
    Notification.send(
        SomeNotification(),
        User.objects.filter(id="example"),
        [DatabaseBackend, EmailBackend]
    )
    """
    @classmethod
    def send(cls, notification, users, backends=None):
        if not isinstance(users, QuerySet):
            users = [users]
        if backends is None:
            backends = notification.backends

        for user in users:
            for backend in backends:
                backend().send(user, notification)
