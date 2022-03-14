from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('email', 'role',)
