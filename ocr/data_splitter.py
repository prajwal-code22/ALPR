import torchvision
from image_transformers import train_transforms

# Loading train and test dataset
train_dataset = torchvision.datasets.EMNIST( root="./data", train=True, download=True, transform=train_transforms, split="byclass")
test_dataset = torchvision.datasets.EMNIST( root="./data", train=False, download=True, transform=train_transforms, split="byclass")
