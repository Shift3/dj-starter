from {{cookiecutter.project_slug}}.users.serializers import UserSerializer
from rest_framework import serializers
from .models import Farm, HistoricalFarm

class FarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farm
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

class FarmHistorySerializer(serializers.ModelSerializer):
    history_user = UserSerializer()

    class Meta:
        model = HistoricalFarm
        fields = "__all__"
