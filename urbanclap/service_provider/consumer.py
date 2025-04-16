from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("🔌 WebSocket connection attempt...")
        
        # Get user ID from URL parameter
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"user_{self.user_id}"
        
        # Check authentication
        user = self.scope["user"]
        if user.is_authenticated:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            print(f"✅ WebSocket connected: {self.group_name}")
        else:
            print("❌ WebSocket connection rejected: Anonymous user")
            await self.close()

    async def disconnect(self, close_code):  # ✅ Correct indentation
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"🔌 WebSocket disconnected: {self.group_name}")

    async def send_notification(self, event):  # ✅ Correct indentation
        print("Received event:", event) 
        print("📨 Sending notification via WebSocket:", event['message'])
        await self.send(text_data=json.dumps(event['message']))