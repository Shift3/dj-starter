import jwt
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden


@database_sync_to_async
def get_user(pk):
    try:
        return get_user_model().objects.get(pk=pk)
    except get_user_model().DoesNotExist:
        return AnonymousUser()


class ShortLivedTokenInQueryStringMiddleware:
    """
    Short-Lived token authorization middleware for Django Channels 3

    Provides Django Channels authentication using short-lived JWT tokens. These
    tokens are issued from /event-token/ and are short-lived (under a minute).
    This token is then used in a `token` query string param during creation of
    the EventSource.

    The flow from the frontend should be:
    
    1) Call `GET /event-token/`
    2) Use the token returned to immediatly open an EventSource like so:
        const evtSource = new EventSource(
            "http://localhost:8000/events/some_user_id_123/?token=the-issued-short-lived-jwt-token"
        );
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        params = parse_qs(scope.get('query_string').decode())
        token = params.get('token', (None,))[0]

        if token:
            try:
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
                scope['user'] = await get_user(decoded['user_id'])
            except jwt.exceptions.ExpiredSignatureError:
                if 'user' in scope:
                    del scope['user']

        return await self.inner(scope, receive, send)
