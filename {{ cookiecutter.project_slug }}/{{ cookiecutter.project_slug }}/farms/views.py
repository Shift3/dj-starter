from .models import Farm
from .serializers import FarmHistorySerializer, FarmSerializer
from {{cookiecutter.project_slug}}.core.filters import (CamelCaseDjangoFilterBackend,
                                                        CamelCaseOrderingFilter)
from {{cookiecutter.project_slug}}.users.models import User
from {{cookiecutter.project_slug}}.users.permissions import IsAnyRole
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.mixins import NestedViewSetMixin


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = (
        IsAuthenticated,
        IsAnyRole([User.EDITOR, User.USER, User.ADMIN]),
    )
    filter_backends = (
        filters.SearchFilter,
        CamelCaseOrderingFilter,
        CamelCaseDjangoFilterBackend,
    )
    filterset_fields = {
        "email": ["icontains", "istartswith", "iendswith", "iexact"],
        "name": ["icontains", "istartswith", "iendswith", "iexact"],
        "phone_number": ["icontains", "istartswith", "iendswith", "iexact"],
    }
    search_fields = ["email", "name", "phone_number"]


class FarmHistoryViewSet(
    NestedViewSetMixin, viewsets.GenericViewSet, mixins.ListModelMixin
):
    serializer_class = FarmHistorySerializer

    def get_queryset(self):
        return self.filter_queryset_by_parents_lookups(
            HistoricalFarm.objects.order_by('-history_date').select_related("history_user")
        )
