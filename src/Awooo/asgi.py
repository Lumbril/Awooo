"""
ASGI config for Awooo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Awooo.settings')

application = get_asgi_application()

from api.websockets.chat_consumer import ChatConsumer

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/<int:user_id>', ChatConsumer.as_asgi())
            ])
        )
    ),
})
