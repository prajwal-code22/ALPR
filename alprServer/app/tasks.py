import json
from app.models import ScannedPlate
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from celery import shared_task
from alprServer.redis import r

p = r.pubsub()
p.subscribe("result")

@shared_task
def listen_result():

    for message in p.listen():
        print("Waiting for result ...")
        channel = message.get("channel")
        data = message.get("data")
        try: 
            channel = channel.decode("utf-8")
        except:
            ...
        print(channel)
        if channel == "result" and message['type'] == 'message':

            json_data = json.loads(data) 
            print(json_data)

            id_ = json_data[0]
            numbers = json_data[1]

            sp = ScannedPlate.objects.get(pk=id_)
            room_name = sp.user.username

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                room_name,
                {
                    'type': 'send_result',
                    'message': numbers
                }
            )


listen_result.delay()