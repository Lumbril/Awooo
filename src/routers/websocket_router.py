from django.urls import re_path

from api.websockets.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<user_id>\w+)/$", ChatConsumer.as_asgi()),
]
