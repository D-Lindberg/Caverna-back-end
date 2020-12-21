from django.core.asgi import get_asgi_application
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

from Cave_Farmers.middleware import TokenAuthMiddlewareStack
from Caverna.consumers import CaveFarmerConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websokect': TokenAuthMiddlewareStack(
        URLRouter([
            path('cavefarmer', CaveFarmerConsumer),
        ])
    ),
})