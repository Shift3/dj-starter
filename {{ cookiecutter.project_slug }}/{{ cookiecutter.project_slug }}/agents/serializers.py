from {{ cookiecutter.project_slug }}.users.serializers import UserSerializer
from rest_framework import serializers
from .models import Agent
from .models import HistoricalAgent


class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agent
        fields = (
            "id",
            "email",
            "name",
            "description",
            "created",
            "modified",
            "phone_number",
            "address1",
            "address2",
            "city",
            "state",
            "zip_code"
        )

class AgentHistorySerializer(serializers.ModelSerializer):
    history_user = UserSerializer()

    class Meta:
        model = HistoricalAgent
        fields = "__all__"
