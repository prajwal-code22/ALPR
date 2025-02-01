import redis
import cv2
from inference_sdk import InferenceHTTPClient
import pickle
from app.license_plate_detector import LicensePlateDetector

r = redis.Redis(host="localhost", port="6379")
p = r.pubsub()



def read_lp_from_image(scanned_plate_id, image: cv2.typing.MatLike):
    # Initialize the license plate detector
    detector = LicensePlateDetector()

    # Get the cropped license plate as a NumPy array
    cropped_plate_array = detector.detect_license_plate(image)
    cv2.imshow('Cropped License Plate', cropped_plate_array)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Encode the cropped plate image to JPEG format
    success, img_encoded = cv2.imencode('.jpg', cropped_plate_array)
    
    if not success:
        print("Failed to encode image")
        return

    # Convert the encoded image to a byte stream
    cropped_plate_bytes = img_encoded.tobytes()

    # Push the image byte stream to Redis along with the scanned plate ID
    img_detail = (scanned_plate_id, cropped_plate_bytes)
    r.publish("image", pickle.dumps(img_detail))

    print("Cropped plate pushed to Redis.")
    return

