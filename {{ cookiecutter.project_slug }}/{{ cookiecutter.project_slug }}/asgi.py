import os

from channels.routing import URLRouter, ProtocolTypeRouter
from django.urls import re_path
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_slug }}.settings.dev")

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

{%- if cookiecutter.include_notifications == "yes" %}
import django_eventstream
from {{ cookiecutter.project_slug }}.core.middleware import TokenInHeaderMiddleware
{%- endif %}


application = ProtocolTypeRouter({
    "http": URLRouter([
{%- if cookiecutter.include_notifications == "yes" %}
        re_path(r"^events/(?P<channel>[\w-]+)/", TokenInHeaderMiddleware(
            URLRouter(django_eventstream.routing.urlpatterns)
        )),
{%- endif %}
        re_path(r"", django_asgi_app),
    ]),
})
