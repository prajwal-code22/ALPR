from torchvision import transforms
from OCR_model import OCRModel

pred_transforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.RandomErasing(p=0.3),
    transforms.Resize((64, 64)),  # Final consistent size
])


model = OCRModel()

