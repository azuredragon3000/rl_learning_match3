import torch
import torch.nn as nn
import torch.optim as optim

# Neural Network Model for Q-Learning
class QNetwork(nn.Module):
    def __init__(self, input_dim, action_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)  # Hidden layer 1
        self.fc2 = nn.Linear(128, 64)        # Hidden layer 2
        self.fc3 = nn.Linear(64, action_dim) # Output layer: Q-values for each action

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)  # Output Q-values
