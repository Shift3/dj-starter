from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from {{ cookiecutter.project_slug }}.core.filters import (
    CamelCaseDjangoFilterBackend,
    CamelCaseOrderingFilter,
)
from {{ cookiecutter.project_slug }}.core.pagination import LinkedCursorPagination
from {{ cookiecutter.project_slug }}.core.serializers import NullSerializer
from .serializers import NotificationSerializer
import jwt

@api_view()
def event_token(request):
    """
    GET's to this endpoint, generate a short-lived token that authorizes
    a user to subscribe to the users event stream.
    """

    encoded = jwt.encode({
        "user_id": str(request.user.id),
        "iat": datetime.now(tz=timezone.utc),
        "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=settings.NOTIFICATION_TOKEN_EXPIRATION_SECONDS)
    }, settings.SECRET_KEY, algorithm="HS256")

    return Response({"token": encoded})


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LinkedCursorPagination
    filter_backends = (
        CamelCaseOrderingFilter,
        CamelCaseDjangoFilterBackend,
    )
    filterset_fields = {
        "read": ["isnull"],
    }
    ordering_fields = ["created"]
    ordering = "-created"

    def get_queryset(self):
        return self.request.user.notifications.all()

    @action(
        detail=False,
        serializer_class=NullSerializer,
        methods=["post"],
    )
    def mark_all_read(self, request):
        user = request.user
        user.notifications.filter(read__isnull=True).update(read=timezone.now())

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        serializer_class=NullSerializer,
        methods=["post"],
    )
    def mark_read(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.read = timezone.now()
        notification.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
