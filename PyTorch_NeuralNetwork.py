import torch.nn as nn
import torch.nn.functional as F

class CNN1(nn.Module):
    def __init__(self):
        super(CNN1, self).__init__()
        #conv layer sees 224x224x3 image tensor
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=5, stride=2, padding=1)
        self.conv2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=5, stride=2, padding=1)
        self.conv3 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=5, stride=1, padding=1)
        self.conv4 = nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=1)
        self.conv5 = nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2,2)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(512,50)
        self.fc2 = nn.Linear(50,2)
        self.dropout = nn.Dropout(0.1)
        
    def forward(self, x):
        #print(x.size())
        x = self.pool(F.relu(self.conv1(x)))
        #print(x.shape)
        x = self.pool(F.relu(self.conv2(x)))
        #print(x.shape)
        x = self.pool(F.relu(self.conv3(x)))
        #print(x.shape)
        x = self.pool(F.relu(self.conv4(x)))
        #print(x.shape)
        x = self.pool(F.relu(self.conv5(x)))
        #print(x.shape)
            
        x = self.flatten(x)
        x = self.dropout(x)
        #print(x.shape)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x

class Net2(nn.Module):
    def __init__(self):
        super(Net2, self).__init__()
        # convolutional layer (sees 224x224x3 image tensor)
        self.flatten = nn.Flatten()
        self.conv1 = nn.Conv2d(3, 24, 5, stride=2, padding=1)
        self.conv2 = nn.Conv2d(24, 32, 5, stride=2, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 5, stride=2, padding=1)
        self.conv4 = nn.Conv2d(64, 64, 3, stride=2, padding=1)
        self.conv5 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64, 50)
        self.fc2 = nn.Linear(50, 2)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        # add sequence of convolutional and max pooling layers
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.pool(F.relu(self.conv4(x)))
        #x = self.pool(F.relu(self.conv5(x)))
        # flatten image input
        x = self.flatten(x)
        x = self.dropout(x)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

class Net(nn.Module):
    def __init__(self):
        super().__init__() #Input = 3,224,224
        self.conv1 = nn.Conv2d(3, 16, kernel_size = 5, padding = 2) #112
        self.conv2 = nn.Conv2d(16, 32, kernel_size = 5, padding = 2) #56
        self.conv3 = nn.Conv2d(32, 64, kernel_size = 5, padding = 2) #28
        self.conv4 = nn.Conv2d(64, 64, kernel_size = 3, stride = 2, padding = 1) #7
        self.pool = nn.MaxPool2d(2,2)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(7*7*64, 1000)
        self.fc2 = nn.Linear(1000,300)
        self.fc3 = nn.Linear(300,50)
        self.fc4 = nn.Linear(50,2)
        self.dropout = nn.Dropout(0.1)
        
        
    def forward(self,x):
        x = self.pool(F.relu(self.conv1(x))) 
        x = self.pool(F.relu(self.conv2(x))) 
        x = self.pool(F.relu(self.conv3(x))) 
        x = self.pool(F.relu(self.conv4(x))) 
        x = self.flatten(x)
        x = self.dropout(x)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.dropout(x)
        x = self.fc3(x)
        x = self.dropout(x)
        x = self.fc4(x)
        
        return x