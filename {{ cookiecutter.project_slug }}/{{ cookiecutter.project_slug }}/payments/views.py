from rest_framework import serializers, status
from rest_framework import mixins, viewsets, fields
from rest_framework.decorators import action
from rest_framework.response import Response
from djstripe.models import PaymentMethod, SetupIntent
from djstripe.models.core import Customer, Product, Price
from djstripe.models.billing import Subscription, InvoiceItem
from django.shortcuts import get_object_or_404
from django.conf import settings
from .serializers import (
    ProductSerializer,
    InvoiceItemSerializer,
    PaymentMethodSerializer,
    ActiveSubscriptionSerializer,
    NullSerializer,
    SubscriptionSerializer,
)
from django.db.models import Q

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class PlanListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Product.objects.filter(active=True).order_by('metadata__order')
    serializer_class = ProductSerializer


class PaymentMethodViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    Provides endpoints regarding the creation and deletion of payment methods.
    """

    pagination_class = None
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NullSerializer
        return PaymentMethodSerializer
    
    def get_queryset(self):
        customer, _ = Customer.get_or_create(self.request.user)
        return customer.payment_methods.all()

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def create(self, request, *args, **kwargs):
        user = request.user
        customer = get_object_or_404(Customer, subscriber=user)

        setup_intent = stripe.SetupIntent.create(
            customer=customer.id,
            usage='off_session',
            payment_method_types=["card"],
        )
        SetupIntent.sync_from_stripe_data(setup_intent)
        return Response(data={
            "client_secret": setup_intent.client_secret
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        customer = get_object_or_404(Customer, subscriber=user)

        payment_method = self.get_object()
        if payment_method not in customer.payment_methods.all():
            return Response(status=status.HTTP_404_NOT_FOUND)

        payment_method.detach()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        methods=['post'],
        detail=True
    )
    def make_default(self, request, *args, **kwargs):
        user = request.user
        customer = get_object_or_404(Customer, subscriber=user)

        customer.default_payment_method = self.get_object()
        customer.save()

        serializer = PaymentMethodSerializer(customer.default_payment_method, context=self.get_serializer_context())
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SubscriptionViewSet(viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def list(self, request, *args, **kwargs):
        user = request.user
        customer, _ = Customer.get_or_create(user)

        invoice_items = InvoiceItem.objects.filter(
            Q(customer=customer),
            Q(invoice__status="paid") | Q(invoice__status="uncollectable"),
        ).order_by('date')
        invoice_item_serializer = InvoiceItemSerializer(invoice_items, many=True)

        payment_methods = customer.payment_methods.all()
        payment_method_serializer = PaymentMethodSerializer(payment_methods, many=True, context=self.get_serializer_context())

        current_subscription = user.subscription
        active_subscription_data = None

        if current_subscription:
            subscription_serializer = ActiveSubscriptionSerializer(current_subscription)
            active_subscription_data = subscription_serializer.data

        # TODO: Sort billing history by DATE

        data = {
            'user' : user.id,
            'customer': customer.id,
            'payment_methods': payment_method_serializer.data,
            'billing_history': invoice_item_serializer.data,
            'active_subscription':  active_subscription_data,
        }

        return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        customer, _ = Customer.get_or_create(user)

        if user.subscription is not None:
            # eventually lets throw an error here with some info.
            return Response(status=status.HTTP_400_BAD_REQUEST)

        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": serializer.data['price_id']}],
            payment_behavior="default_incomplete",
            expand=['latest_invoice.payment_intent'],
        )
        Subscription.sync_from_stripe_data(subscription)

        return Response(data={
            "client_secret": subscription.latest_invoice.payment_intent.client_secret,
            "subscription_id": subscription.id,
        }, status=status.HTTP_201_CREATED)

    @action(
        methods=['post'],
        detail=False,
        serializer_class=NullSerializer,
    )
    def reactivate(self, request, *args, **kwargs):
        user = request.user
        customer = get_object_or_404(Customer, subscriber=user)
        current_subscription = user.subscription

        if not current_subscription.is_status_temporarily_current():
            return Response(status=status.HTTP_404_NOT_FOUND)

        current_subscription.reactivate()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post'],
        detail=False,
        serializer_class=NullSerializer,
    )
    def cancel(self, request, *args, **kwargs):
        user = request.user
        current_subscription = user.subscription
        current_subscription.cancel(True)

        return Response(status=status.HTTP_204_NO_CONTENT)
