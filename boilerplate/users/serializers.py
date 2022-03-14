from rest_framework import serializers
from .models import User
from djoser import serializers as dj_serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email', 'role', 'profile_picture', 'created',
            'modified', 'first_name', 'last_name', 'activated_at'
        )


class UserCreateSerializer(dj_serializers.UserCreateSerializer):

    def validate(self, attrs):
        validated_data = super()
        user = self.context['request'].user
        requested_role = attrs.get('role')
        breakpoint()
        return validated_data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'email', 'auth_token',)
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}
