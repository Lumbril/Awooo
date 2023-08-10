from django.urls import path

from api.websockets.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    path('ws/<int:user_id>', ChatConsumer.as_asgi()),
]
