from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from .agents.views import AgentHistoryViewSet, AgentViewSet
from .users.views import UserHistoryViewSet, UserViewSet
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


class DefaultRouterWithNesting(NestedRouterMixin, DefaultRouter):
    pass


router = DefaultRouterWithNesting()
(
    router.register(r"agents", AgentViewSet)
          .register(r"history", AgentHistoryViewSet, "agent_history", parents_query_lookups=["id"])
)
(
    router.register(r"users", UserViewSet)
          .register(r"history", UserHistoryViewSet, "user_history", parents_query_lookups=["id"])
)

urlpatterns = [
    path("health-check", include("health_check.urls")),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include("djoser.urls.authtoken")),
    path("rf-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
