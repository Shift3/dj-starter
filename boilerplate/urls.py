from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from .agents.views import AgentViewSet
from .users.views import UserViewSet
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

router = DefaultRouter()
router.register(r'agents', AgentViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include('djoser.urls.authtoken')),
    path('rf-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')), )
