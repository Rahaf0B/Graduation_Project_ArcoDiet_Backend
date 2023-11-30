
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatAPI.jwtAuth import JWTAuthMiddleware
import chatAPI.routing as chatRoute

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArcoDiet.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':JWTAuthMiddleware(
        URLRouter(
            chatRoute.websocket_urlpatterns,
        )
    )
})







# """
# ASGI config for ArcoDiet project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArcoDiet.settings')

# application = get_asgi_application()
