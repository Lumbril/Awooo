from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from jwt import decode as jwt_decode
from django.conf import settings

from packs.services.get_user_async import get_user


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, *args, **kwargs):
        headers = dict(
            (key.decode("utf-8"), value.decode("utf-8"))
            for key, value in scope['headers']
        )
        token = headers['authorization']

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            return None

        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=['HS512'])
        scope["user"] = await get_user(validated_token=decoded_data)

        return await super().__call__(scope, *args, **kwargs)
