from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import service_provider.routing

application = ProtocolTypeRouter({
    "http": URLRouter([
        # You can add standard HTTP routes here if needed
    ]),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            service_provider.routing.websocket_urlpatterns
        )
    ),
})
