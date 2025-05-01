import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import time
import os

class SimpleMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)
    def forward(self, x):
        x = x.view(-1, 28 * 28)
        x = self.relu(self.fc1(x))
        return self.fc2(x)

def train_from_pt():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load the raw tensors
    processed_dir = os.path.join('MNIST', 'processed')
    train_data, train_targets = torch.load(os.path.join(processed_dir, 'training.pt'))
    # Convert to float in [0,1], then normalize
    train_data = train_data.unsqueeze(1).float().div(255.)
    mean, std = 0.1307, 0.3081
    train_data = (train_data - mean) / std

    # Build a dataset + loader
    train_ds = TensorDataset(train_data, train_targets)
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)

    model = SimpleMLP().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    num_epochs = 3

    start_time = time.time()
    model.train()
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        for data, target in train_loader:
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            loss = criterion(model(data), target)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        print(f"Epoch {epoch+1}/{num_epochs} — Loss: {epoch_loss/len(train_loader):.4f}")
    print(f"Training time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    train_from_pt()
