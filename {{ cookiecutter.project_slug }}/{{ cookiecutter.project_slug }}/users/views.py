from rest_framework_extensions.mixins import NestedViewSetMixin
from {{ cookiecutter.project_slug }}.users.email import ChangeEmailRequestEmail
from {{ cookiecutter.project_slug }}.core.filters import (
    CamelCaseDjangoFilterBackend,
    CamelCaseOrderingFilter,
)
from djoser.serializers import UidAndTokenSerializer
from django.db import transaction
from rest_framework import filters, status, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.conf import settings
from djoser import signals
from djoser.compat import get_user_email
from .serializers import (
    ChangeEmailRequestSerializer,
    InviteUserSerializer,
    ProfilePictureSerializer,
    UserSerializer,
    UserHistorySerializer
)
from .permissions import IsAdmin, IsUserOrAdmin
from .models import HistoricalUser


class UserViewSet(DjoserUserViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (
        filters.SearchFilter,
        CamelCaseOrderingFilter,
        CamelCaseDjangoFilterBackend,
    )
    filterset_fields = {
        "email": ["icontains", "istartswith", "iendswith", "iexact"],
        "last_name": ["icontains", "istartswith", "iendswith", "iexact"],
        "first_name": ["icontains", "istartswith", "iendswith", "iexact"],
        "role": ["in", "isnull"],
        "activated_at": ["gt"],
    }
    search_fields = ["email", "last_name", "first_name"]

    def perform_update(self, serializer):
        serializer.save()

    @action(
        detail=False,
        methods=["post"],
        serializer_class=ChangeEmailRequestSerializer,
        permission_classes=[IsAuthenticated, IsUserOrAdmin],
    )
    def change_email_request(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        self.check_object_permissions(request, user)

        user.new_email = serializer.data["email"]
        user.save()

        context = {"user": user}
        to = [user.new_email]
        ChangeEmailRequestEmail(request, context).send(to)

        return Response(status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=UidAndTokenSerializer,
        permission_classes=[IsUserOrAdmin],
    )
    def confirm_change_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        self.check_object_permissions(request, serializer.user)

        # TODO: check that unique key failure results in a sensible response
        user.email = user.new_email
        user.new_email = None
        user.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsUserOrAdmin])
    def resend_change_email_request_email(self, request, id=None):
        user = self.get_object()
        if user.new_email is not None:
            context = {"user": user}
            to = [user.new_email]
            ChangeEmailRequestEmail(request, context).send(to)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=True,
        methods=["post"],
        parser_classes=(
            FormParser,
            MultiPartParser,
        ),
    )
    def profile_picture(self, request, id=None):
        serializer = ProfilePictureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()

        # Delete old profile picture if it exists
        user.delete_profile_picture(save=False)

        user.profile_picture = request.data["file"]
        user.save()

        serialized_user = UserSerializer(user, context={"request": request})
        return Response(data=serialized_user.data, status=status.HTTP_200_OK)

    @profile_picture.mapping.delete
    def delete_profile_picture(self, request, id=None):
        user = self.get_object()

        user.delete_profile_picture(save=True)

        serialized_user = UserSerializer(user, context={"request": request})
        return Response(data=serialized_user.data, status=status.HTTP_200_OK)

    # Overrides djoser provided activation view with our own, which
    # sets the users password during activation.
    @action(["post"], detail=False, permission_classes=[AllowAny])
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.activate()
        user.set_password(serializer.data["password"])
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.confirmation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAdmin],
        serializer_class=InviteUserSerializer,
    )
    @transaction.atomic
    def invitation(self, request):
        serializer = InviteUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.is_active = False
        user.save(update_fields=["is_active"])

        # Send invitation email
        context = {"user": user}
        to = [user.email]
        settings.EMAIL.activation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserHistoryViewSet(
    NestedViewSetMixin, viewsets.GenericViewSet, mixins.ListModelMixin
):
    serializer_class = UserHistorySerializer

    def get_queryset(self):
        return self.filter_queryset_by_parents_lookups(
            HistoricalUser.objects.order_by('-history_date').select_related("history_user")
        )
