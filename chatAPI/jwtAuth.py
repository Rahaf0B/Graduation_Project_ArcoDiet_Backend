import jwt
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.contrib.auth import get_user_model
from reqUser.models import User
from asgiref.sync import sync_to_async
class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token = headers[b'authorization'].decode('utf-8').split(" ")[1]
                payload = jwt.decode(token, settings.SECRET_KEY,algorithms="HS256")
                email = payload['email']
                scope['user'] = await self.get_user(email)
            except (jwt.exceptions.DecodeError, User.DoesNotExist):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        return await self.inner(scope, receive, send)

    async def get_user(self, email):
        try:
            return await sync_to_async( User.objects.get)(email=email)
        except User.DoesNotExist:
            return AnonymousUser()