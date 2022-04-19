from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.db import transaction
from {{ cookiecutter.project_slug }}.core.models import Address
from phonenumber_field.phonenumber import to_python
from .models import Agent

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('address1', 'address2', 'city', 'state', 'zip_code')


class AgentSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)

    class Meta:
        model = Agent
        fields = (
            'id', 'email', 'name', 'description', 'created', 'modified',
            'phone_number', 'address'
        )

    def _create_or_update_address(self, instance, address_data):
        # Handle deleting address if it absent
        if address_data is None:
            if instance.address is not None:
                instance.address.delete()
                instance.address = None

            instance.save()
            return

        # Handle updating address in validated_data
        if instance.address is None:
            instance.address = Address(**address_data)
        else:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)

        instance.address.save()


    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        instance = Agent()
        # Set regular attrs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        self._create_or_update_address(instance, address_data)

        instance.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        # Set regular attrs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        self._create_or_update_address(instance, address_data)

        instance.save()
        return instance
