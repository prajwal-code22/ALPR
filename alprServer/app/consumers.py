import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class WsConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "room"

        self.room_group_name = f"{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
       async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None):
        try:
            text_data_json = json.loads(text_data)
        except: 
            text_data_json = text_data

        print("received: ", text_data_json)
        self.send(text_data="Message is received "+text_data_json)

    # Receive message from room group
    def send_result(self, event):

        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"numbers": message}))
