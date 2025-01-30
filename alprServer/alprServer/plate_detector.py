import after_response
import redis
import json

r=redis.Redis(host="localhost", port="6379")
p = r.pubsub()
p.subscribe("path")

def publish_to_queue(file_path: str, id_):

    r.publish("path", json.dumps({'path': file_path, 'id': id_}))


@after_response.enable
def detect_plate(file_path, id_):

    # read file from file_path
    # crop license plate
    # Store only the image of license plate with the same file name.

    publish_to_queue(file_path, id_)

    ...