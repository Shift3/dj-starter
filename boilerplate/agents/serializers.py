from rest_framework import serializers
from .models import Agent


class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agent
        fields = (
            'id', 'email', 'name', 'description', 'created', 'modified',
            'phone_number',
        )
