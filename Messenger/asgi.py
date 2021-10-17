import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chatapp.consumers import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Messenger.settings')

application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : AuthMiddlewareStack(
        URLRouter([
            path("wss/room/<str:room_name>/",Chat.as_asgi()),
            path("wss/status/",Status.as_asgi()),
            path("wss/typing/",Typing.as_asgi()),
        ])
    )
})
