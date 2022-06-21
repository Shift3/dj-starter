from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from django_extensions.db.models import TimeStampedModel


class DatabaseNotification(TimeStampedModel, models.Model):
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
    @classmethod
    def send(cls, notification, users, backends=[]):
        if not isinstance(users, QuerySet):
            users = [users]

        for user in users:
            for backend in backends:
                backend().send(user, notification)
