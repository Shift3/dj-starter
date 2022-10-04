from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http.cookie import parse_cookie


@database_sync_to_async
def get_user(token_key):
    try:
        return get_user_model().objects.get(auth_token__key=token_key)
    except get_user_model().DoesNotExist:
        return AnonymousUser()


class TokenInHeaderMiddleware:
    """
    Token authorization middleware for Django Channels 3

    Provides Django Channels authentication using Tokens (e.g. from the Django
    REST framework (DRF) Auth Tokens). The token can be provided in two
    different ways:

        1) HTTP "Authorization" Header containing "Token: <token_value>"
        2) A Cookie with key "x-auth-token" and value "<token_value>"

    If a "Authorization" header is present only this will be used (even if it
    doesn't contain a "Token"). The cookie value will only be checked if the
    "Authorization" header is absent.

    In Javascript there is no way to send any custom headers when using SSE
    and therefore the cookies need to be used:

        document.cookie = 'x-auth-token=36f69f49b6939...478aa; path=/; SameSite=None; Secure';
        const evtSource = new EventSource("http://localhost:8000/events/test123/", { withCredentials: true } );
    """

    HEADER: bytes = b'authorization'
    HEADER_TOKEN_KEY: str = 'Token'
    COOKIE_TOKEN_KEY: str = 'x-auth-token'

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])

        print(headers)
        if self.HEADER in headers:
            token_name, _token_key = headers[self.HEADER].decode().split(':')
            token_key = _token_key.lstrip()
            if token_name == self.HEADER_TOKEN_KEY:
                scope['user'] = await get_user(token_key)

        elif b'cookie' in headers:
            cookies = parse_cookie(headers[b'cookie'].decode())
            cookies_lower = {k.lower(): v for k, v in cookies.items()}
            token_key = cookies_lower.get(self.COOKIE_TOKEN_KEY)
            if token_key:
                scope['user'] = await get_user(token_key)

        return await self.inner(scope, receive, send)
