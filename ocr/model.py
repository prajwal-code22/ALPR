import torch.nn as nn
import torch
from datetime import datetime
import os

class OCRModel(nn.Module):
    def __init__(self, num_classes: int, optimizer, criterion):
        super().__init__()

        self.device = torch.device( 'cuda:0' if torch.cuda.is_available() else 'cpu' )
        self.optimizer = optimizer
        self.criterion = criterion

        self.image_conv_net = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),  # --> 32x64x64
            nn.ReLU(),
            nn.MaxPool2d(2,2), # --> 32x32x32

            nn.Conv2d(32, 16, kernel_size=3, padding=1), # --> 16x32x32
            nn.ReLU(),
            nn.MaxPool2d(2,2),    # --> 16x16x16

            nn.Conv2d(16, 10, kernel_size=3 , padding=1), # --> 10x16x16
            nn.ReLU(),
            nn.MaxPool2d(2,2), # --> 10x8x8

            nn.Flatten() # --> 10x8x8
        )

        self.fc_layer = nn.Sequential(
            nn.Linear(10*8*8, 10),
            nn.ReLU(),

            nn.BatchNorm1d(10), # Normalizes each batch, that is, tries to make input distribution equal to output distribution.

            nn.Linear(10, 10),
            nn.ReLU(),

            nn.Dropout(.3), # Randomly drops some neurons with prob. of 3% reducing chances of overfitting

            nn.Linear(10, 5),
            nn.ReLU(),

            nn.Linear(5, num_classes)
        )

    def forward(self, features):
        out = self.image_conv_net(features)
        out = self.fc_layer(out)

        return out


    def start_train_loop(self, epoch: 10, train_dataloader):
        # Training loop
        epoch_loss_store = []
        for i in range(epoch):
            running_loss = .0
            for features, labels in train_dataloader:

                features = features.to(self.device)
                labels = labels.to(self.device)

                # Forward pass and loss calcuation
                outputs = self(features)
                loss = self.criterion(outputs, labels)

                # Backward pass ans optimizing
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                running_loss += loss.item()

            running_loss /= len(train_dataloader)
            print(f"Epoch: {i+1}, Loss: {running_loss} ")
            epoch_loss_store.append(running_loss)
            
            # Saving model in every 1 epoch
            print("Saving model...")
            self.save_model(self, epoch=i)


    # Saving model
    def save_model(model, epoch: int, final_model: bool=False):
        cdt = datetime.now()
        now = cdt.strftime("%Y-%m-%d_%H_%M_%S")
        saving_dir = "./drive/MyDrive/intermediate-models"

        try:
            os.mkdir(saving_dir)
        except:
            pass
        model_name = f"{epoch}-{now}.pth" if not final_model else f"{epoch}-final.pth"
        torch.save(model, f"{saving_dir}/{model_name}")
