from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from djangorestframework_camel_case.util import camel_to_underscore, underscore_to_camel
from djangorestframework_camel_case.settings import api_settings


class CamelCaseOrderingFilter(OrderingFilter):
    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [
                camel_to_underscore(
                    field.strip(),
                    **api_settings.JSON_UNDERSCOREIZE,
                )
                for field in params.split(",")
            ]
            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering

        return self.get_default_ordering(view)


class CamelCaseDjangoFilterBackend(DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        res = super().get_filterset_kwargs(request, queryset, view)

        filterset_class = self.get_filterset_class(view, queryset)
        query_params = request.query_params.copy()

        # Camel cased items that, when underscored, are valid filter
        # keys to filter by are transformed during this step.
        for param, value in request.query_params.items():
            underscored_param = None
            if "__" in param:
                underscored_part = camel_to_underscore(param.split("__")[0])
                rest = "__".join(param.split("__")[1:])
                underscored_param = f"{underscored_part}__{rest}"
            else:
                underscored_param = camel_to_underscore(param)

            if underscored_param in filterset_class.base_filters.keys():
                if underscored_param not in query_params.keys():
                    query_params[underscored_param] = value

        res["data"] = query_params

        return res
