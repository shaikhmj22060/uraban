# myapp/routing.py
from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path("ws/notifications/<int:user_id>/", consumer.NotificationConsumer.as_asgi()),
]