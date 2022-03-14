from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from django_filters import rest_framework as filters

from boilerplate.users.permissions import IsAdmin
from .models import Agent
from .serializers import AgentSerializer

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return True


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('name', 'email', 'phone_number',)
