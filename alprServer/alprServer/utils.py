import cv2
from inference_sdk import InferenceHTTPClient
import pickle
from .redis import r

p = r.pubsub()
p.subscribe('result')

def read_lp_from_image( scanned_plate_id, image: cv2.typing.MatLike):

    CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="8mgpiuosrxccI2KvBjjS"
    )

    result = CLIENT.infer(image, model_id="license-plate-recognition-rxg4e/6")

# Ensure predictions exist
    if result["predictions"]:
        # Extract bounding box from response
        plate_data = result["predictions"][0]  # Taking the first detected plate
        x, y, w, h = plate_data["x"], plate_data["y"], plate_data["width"], plate_data["height"]
    
        # Convert to integer
        x, y, w, h = int(x), int(y), int(w), int(h)
    
        # Crop the license plate
        cropped_plate = image[y - h//2 : y + h//2, x - w//2 : x + w//2]

        img_detail = (scanned_plate_id, cropped_plate)

        r.publish("image", pickle.dumps(img_detail))