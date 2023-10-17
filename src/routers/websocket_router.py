from django.urls import path

from api.websockets.websocket_consumer import WebSocketConsumer

websocket_urlpatterns = [
    path('ws', WebSocketConsumer.as_asgi()),
]
