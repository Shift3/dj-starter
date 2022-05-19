from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from {{ cookiecutter.project_slug }}.core.filters import CamelCaseDjangoFilterBackend, CamelCaseOrderingFilter
from {{ cookiecutter.project_slug }}.users.permissions import IsAnyRole
from .models import Agent
from {{ cookiecutter.project_slug }}.users.models import User
from .serializers import AgentSerializer


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = (IsAuthenticated, IsAnyRole([User.EDITOR, User.USER, User.ADMIN]),)
    filter_backends = (
        filters.SearchFilter,
        CamelCaseOrderingFilter,
        CamelCaseDjangoFilterBackend,
    )
    filterset_fields = {
        'email': ['icontains', 'startswith', 'endswith', 'exact'],
        'name': ['icontains', 'startswith', 'endswith', 'exact'],
        'phone_number': ['icontains', 'startswith', 'endswith', 'exact'],
    }
    search_fields = ['email', 'name', 'phone_number']

