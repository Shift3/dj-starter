from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from boilerplate.core.filters import CamelCaseDjangoFilterBackend, CamelCaseOrderingFilter
from boilerplate.users.permissions import IsAnyRole
from .models import Agent
from boilerplate.users.models import User
from .serializers import AgentSerializer


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = (IsAuthenticated, IsAnyRole([User.EDITOR, User.USER, User.ADMIN]),)
    filter_backends = (CamelCaseDjangoFilterBackend, CamelCaseOrderingFilter,)
    filterset_fields = {
        'email': ['icontains', 'startswith', 'endswith', 'exact'],
        'name': ['icontains', 'startswith', 'endswith', 'exact'],
        'phone_number': ['icontains', 'startswith', 'endswith', 'exact'],
    }
