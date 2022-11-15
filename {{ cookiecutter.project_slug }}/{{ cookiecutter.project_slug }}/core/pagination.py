import math
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from django.conf import settings


class LinkedPagination(pagination.PageNumberPagination):
    max_page_size = getattr(settings, "PAGINATION_MAX_PAGE_SIZE", None)
    page_size_query_param = "pageSize"

    def get_paginated_response(self, data):
        url = self.request.build_absolute_uri()
        first_page = 1
        page_count = math.ceil(self.page.paginator.count / self.page.paginator.per_page)
        last_page = max(page_count, 1)

        return Response(
            {
                "meta": {
                    "pageCount": page_count,
                    "pageSize": self.page.paginator.per_page,
                    "page": self.page.number,
                    "count": self.page.paginator.count,
                },
                "links": {
                    "first": replace_query_param(url, self.page_query_param, first_page),
                    "next": self.get_next_link(),
                    "prev": self.get_previous_link(),
                    "last": replace_query_param(url, self.page_query_param, last_page),
                },
                "results": data,
            }
        )


class LinkedCursorPagination(pagination.CursorPagination):
    max_page_size = getattr(settings, "PAGINATION_MAX_PAGE_SIZE", None)
    page_size_query_param = "pageSize"

    def paginate_queryset(self, queryset, request, view=None):
        self.count = queryset.count()
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            {
                "meta": {
                    "pageCount": math.ceil(
                        self.count / self.page_size
                    ),
                    "pageSize": self.page_size,
                    "page": None,
                    "count": self.count,
                },
                "links": {
                    "first": "",
                    "next": self.get_next_link(),
                    "prev": self.get_previous_link(),
                    "last": "",
                },
                "results": data,
            }
        )
