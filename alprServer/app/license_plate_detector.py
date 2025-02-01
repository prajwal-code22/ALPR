from ultralytics import YOLO
from django.conf import settings

class LicensePlateDetector:
    def __init__(self):
        self.model_path = f"{settings.MODEL_DIR}/license_plate_detector.pt"
        
        """Initialize the YOLO model only once"""
        self.model = YOLO(self.model_path)

    def detect_license_plate(self, image):
        """Detect and crop the license plate from an image"""

        
        # Perform inference
        results = self.model(image)
        result = results[0]

        # Extract bounding boxes
        if hasattr(result, "boxes") and result.boxes.xyxy is not None:
            for box in result.boxes:
                # Convert tensor to list
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                # Crop the license plate from the image
                license_plate = image[y1:y2, x1:x2]
                return license_plate

        print("No license plate detected.")
        return None


