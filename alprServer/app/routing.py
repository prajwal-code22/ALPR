from django.urls import path
from . import consumers
websocket_urlpatterns = [
    path("", consumers.WsConsumer.as_asgi()),
]