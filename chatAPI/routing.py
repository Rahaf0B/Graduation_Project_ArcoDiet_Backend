

from django.urls import re_path ,path
from . import consumer

websocket_urlpatterns = [
    path(r'ws/socket-server/<int:partner>/', consumer.ChatConsumer.as_asgi())
]





