from torchvision import transforms

auto_contrast_probability = .5

train_transforms = transforms.Compose([
    transforms.RandomAutocontrast(auto_contrast_probability),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),  # Apply before Grayscale
    transforms.RandomRotation(degrees=10),
    transforms.RandomResizedCrop(size=(128, 256), scale=(0.9, 1.0)),
    transforms.Grayscale(),  # Convert after color transforms
    transforms.RandomPerspective(distortion_scale=0.1, p=0.5),
    transforms.GaussianBlur(kernel_size=3),
    transforms.RandomAffine(degrees=5, translate=(0.1, 0.1), scale=(0.9, 1.1), shear=10),
    transforms.ToTensor(),
    transforms.RandomErasing(p=0.3),
    transforms.Resize((64, 64)),  # Final consistent size

])
