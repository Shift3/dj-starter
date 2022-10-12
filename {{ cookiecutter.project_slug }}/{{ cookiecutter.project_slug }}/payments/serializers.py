from rest_framework import serializers, status
from rest_framework import mixins, viewsets, fields
from rest_framework.decorators import action
from rest_framework.response import Response
from djstripe.models import PaymentMethod
from djstripe.models.core import Customer, Product, Price
from djstripe.models.billing import Subscription, InvoiceItem
from django.shortcuts import get_object_or_404
from django.conf import settings

class PlanSerializer(serializers.Serializer):
    id = fields.CharField()
    interval = fields.CharField()
    amount = fields.DecimalField(decimal_places=2, max_digits=10)
    product = fields.CharField()


class SubscriptionSerializer(serializers.Serializer):
    price_id = fields.CharField()


class ActiveSubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Subscription
        fields = ["id", "current_period_end", "plan", "canceled_at"]


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ["amount", "date", "description"]


class PaymentMethodSerializer(serializers.ModelSerializer):
    is_default = serializers.SerializerMethodField('_is_default')

    def _is_default(self, obj):
        request = self.context['request']
        user = request.user
        customer = Customer.objects.get(subscriber=user)
        return customer.default_payment_method == obj
    
    class Meta:
        model = PaymentMethod
        fields = ["id", "type", "card", "is_default"]


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            'unit_amount', 'currency', 'nickname', 'metadata', 'type', 'recurring', 'id'
        )


class ProductSerializer(serializers.ModelSerializer):
    """
    The job of this class is to turn `Product` objects into JSON
    """
    prices = PriceSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'metadata', 'prices'
        )


class NullSerializer(serializers.Serializer):
    pass