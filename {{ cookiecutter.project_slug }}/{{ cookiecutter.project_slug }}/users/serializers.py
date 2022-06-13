from {{ cookiecutter.project_slug }}.core.fields import ThumbnailField
from rest_framework import serializers
from djoser import serializers as dj_serializers
from djoser.conf import settings as djoser_settings
from .models import User, HistoricalUser


class ActivationSerializer(dj_serializers.ActivationSerializer):
    password = serializers.CharField()
    password_confirmation = serializers.CharField()

    def validate_password(self, value):
        if value != self.initial_data["password_confirmation"]:
            raise serializers.ValidationError("Passwords must match.")
        return value


class UserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailField()

    class Meta:
        model = User
        read_only_fields = ("id", "activated_at", "created", "modified", "new_email")
        fields = (
            "id",
            "activated_at",
            "created",
            "modified",
            "email",
            "role",
            "profile_picture",
            "first_name",
            "last_name",
            "new_email",
        )


class ChangeEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class InviteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "role")


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_picture",)


class TokenSerializer(dj_serializers.TokenSerializer):
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    token = serializers.CharField(source="key")

    class Meta:
        model = djoser_settings.TOKEN_MODEL
        fields = ("token", "user")


class UserHistorySerializer(serializers.ModelSerializer):
    history_user = UserSerializer()

    class Meta:
        model = HistoricalUser
        fields = "__all__"
