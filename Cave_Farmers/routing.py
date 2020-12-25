from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from Caverna.routing import websocket_urlpatterns as caverna_ws_url_patterns

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websokect': AuthMiddlewareStack(URLRouter(caverna_ws_url_patterns)),
})