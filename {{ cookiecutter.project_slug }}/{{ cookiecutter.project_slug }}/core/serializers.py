from {{ cookiecutter.project_slug }}.notification_system.models import DatabaseNotification
from rest_framework import serializers


class NullSerializer(serializers.Serializer):
    pass


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseNotification
        fields = ["type", "data", "read", "created"]
