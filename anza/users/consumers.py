import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # set up groups and add the user to the group
        self.group_name = 'notification'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        await self.send(text_data=json.dumps({
            'message': 'Connection created'
        }))

    async def disconnect(self, close_code):
        # remove the user from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def send_notification(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))