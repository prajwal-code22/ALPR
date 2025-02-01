import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from celery import shared_task
from alprServer.redis import r

p = r.pubsub()
p.subscribe("result")

@shared_task
def listen_result():

    for message in p.listen():

        channel = message.get("channel")
        data = message.get("data")
        try: 
            channel = channel.decode("utf-8")
        except:
            ...

        if channel == "result" and message['type'] == 'message':

            json_data = json.loads(data) 

            numbers = json_data[1]

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "room",
                {
                    'type': 'send_result',
                    'message': numbers
                }
            )


listen_result.delay()