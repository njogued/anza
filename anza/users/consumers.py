import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # set up groups and add the user to the group
        user = self.scope['user']
        if user.is_authenticated:
            self.user_id = user.id
            print(user.id)
            self.group_name = f'notify_{self.user_id}'
            await self.channel_layer.group_add(
                self.group_name, # group to add user to
                self.channel_name # relates to one user
            )
            await self.accept()
            message = f'Connection created for user id: {self.user_id}'
            await self.send(text_data=json.dumps({
                'message': message
            }))
        else:
            self.user_id = None

    async def receive(self, data):
        # receive and send messages, typically from FE
        # FE JS code
        # ws.send(JSON.stringify({
        #     "message": "some message"
        # }))
        data_json = json.loads(data)
        message = data_json['message']
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_notification',
                'message': message
            }
        )

    async def disconnect(self, close_code):
        # remove the user from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def send_notification(self, data):
        # send a notification
        await self.send(text_data=json.dumps({'message': data['message']}))

def send_user_notification(info):
    # send notification to specific user
    channel_layer = get_channel_layer()
    user_id = info['user']
    group_name = f'notify_{user_id}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'message': info['message']
        }
    )
