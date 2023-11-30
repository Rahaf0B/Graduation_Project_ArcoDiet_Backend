from datetime import date
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Massage, UploadedImage
from reqUser.models import User
from PIL import Image
from io import BytesIO
import base64
from django.core.files.base import ContentFile


class ChatConsumer(WebsocketConsumer):
    massageTime = None

    def connect(self):
        self.partner = self.scope['url_route']['kwargs']['partner']
        user = self.scope["user"]
        FID = 0
        SID = 0
        if (self.partner > user.user_id):
            FID = self.partner
            SID = user.user_id

        else:
            FID = user.user_id
            SID = self.partner

        self.room_group_name = "group_{}_{}".format(FID, SID)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data):

        user = self.scope["user"]
        message = ""
        data = json.loads(text_data)
        if data['type'] == 'image_upload':
            image_data = data['image']

            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            image_resized = image.resize((500, 500))
            message_image = Massage()
            image_byte_array = BytesIO()
            image_resized.save(image_byte_array, format='PNG')
            message_image.sender = user

            message_image.receiver = User.objects.get(user_id=self.partner)
            message_image.type = data['type']

            message_image.image.save(
                'send_image.png', ContentFile(image_byte_array.getvalue()))
            massageTime = message_image.timestamp

            response = {
                'type': 'image_message',
                'message': message_image.image.url,
                'sender_id': user.user_id,
                'time': massageTime
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'image_message',
                    'message': message_image.image.url,
                    'sender_id': user.user_id,
                    'time': massageTime
                }
            )

        else:

            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            msgModel = Massage()
            msgModel.sender = user

            msgModel.receiver = User.objects.get(user_id=self.partner)
            msgModel.massage = message
            msgModel.type = data['type']
            msgModel.save()
            massageTime = msgModel.timestamp

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'sender_id': user.user_id,
                    'type': 'chat_message',
                    'message': message,
                    'time': massageTime
                }
            )

    def chat_message(self, event):

        message = event['message']
        self.send(text_data=json.dumps({
            'sender_id': event['sender_id'],
            'type': 'chat',
            'message': message,
            'time': event['time'].strftime("%H:%M"),
            "date": event['time'].strftime("%m-%d-%Y"),
            "type": "text",



        }))

    def image_message(self, event):
        self.send(text_data=json.dumps({'type': 'image_message',
                                        'sender_id': event['sender_id'],
                                        'message': event["message"],
                                        'time': event['time'].strftime("%H:%M"),
                                        "date": event['time'].strftime("%m-%d-%Y"),
                                        }))
