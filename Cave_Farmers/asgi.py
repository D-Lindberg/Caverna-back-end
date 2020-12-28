"""
ASGI config for Cave_Farmers project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from Caverna.routing import websocket_urlpatterns as caverna_ws_url_patterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cave_Farmers.settings')

#django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websokect': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                caverna_ws_url_patterns
            )
        ),
    ),
})
