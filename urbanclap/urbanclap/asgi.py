import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import service_provider.routing  # replace with your actual app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urbanclap.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            service_provider.routing.websocket_urlpatterns
        )
    ),
})