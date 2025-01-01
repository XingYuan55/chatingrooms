import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chating.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chat.consumers import ChatConsumer
from channels.security.websocket import AllowedHostsOriginValidator

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/chat/', ChatConsumer.as_asgi()),
            ])
        )
    ),
}) 