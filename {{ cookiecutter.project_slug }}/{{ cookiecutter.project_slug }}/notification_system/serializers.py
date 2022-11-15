from rest_framework import serializers
from .models import DatabaseNotification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseNotification
        fields = ["id", "type", "data", "read", "created"]
