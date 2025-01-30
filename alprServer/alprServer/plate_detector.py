# import after_response
import asyncio
import redis
import json
import cv2
from inference_sdk import InferenceHTTPClient


r=redis.Redis(host="localhost", port="6379")
p = r.pubsub()
p.subscribe("path")

def publish_to_queue(file_path: str, id_, file_type):

    r.publish("path", json.dumps({'path': file_path, 'id': id_, 'type': file_type}))


# @after_response.enable
def detect_plate(file_path, id_, file_type):
    CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="8mgpiuosrxccI2KvBjjS"
    )
    image_url = file_path
    result = CLIENT.infer(image_url, model_id="license-plate-recognition-rxg4e/6")
    image = cv2.imread(file_path)

# Ensure predictions exist
    if result["predictions"]:
        # Extract bounding box from response
        plate_data = result["predictions"][0]  # Taking the first detected plate
        x, y, w, h = plate_data["x"], plate_data["y"], plate_data["width"], plate_data["height"]
    
        # Convert to integer
        x, y, w, h = int(x), int(y), int(w), int(h)
    
        # Crop the license plate
        cropped_plate = image[y - h//2 : y + h//2, x - w//2 : x + w//2]
    
        # Save the cropped plate
        cv2.imwrite(file_path, cropped_plate)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        publish_to_queue(file_path, id_, file_type)
    
