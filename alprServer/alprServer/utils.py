import cv2
import pickle
from .redis import r
from app.license_plate_detector import LicensePlateDetector
p = r.pubsub()

detector = LicensePlateDetector()
def read_lp_from_image(scanned_plate_id, image: cv2.typing.MatLike):

    # Get the cropped license plate as a NumPy array
    cropped_plate = detector.detect_license_plate(image)

    # Push the image byte stream to Redis along with the scanned plate ID
    img_detail = (scanned_plate_id, cropped_plate)

    r.publish("image", pickle.dumps(img_detail))
