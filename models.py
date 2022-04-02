import torch
import torch.nn as nn

class DeepTP(nn.Module):    
    def __init__(self, out_features=[0],li = [[4, 16], [8, 12]]):
        super(DeepTP, self).__init__()
        self.explainECs = out_features
        self.layer_info = li
        self.cnn0 = CNN(self.layer_info)
        self.fc1 = nn.Linear(in_features=128*3, out_features=512)
        self.bn1 = nn.BatchNorm1d(num_features=512)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(in_features=512, out_features=len(out_features))
        self.bn2 = nn.BatchNorm1d(num_features=len(out_features))
        self.out_act = nn.Sigmoid()
        self.init_weights()


    def init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.xavier_uniform_(m.weight)
            elif isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)

    def forward(self, x):
        x = self.cnn0(x)
        x = x.view(-1, 128*3)
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.out_act(self.bn2(self.fc2(x)))
        return x


class CNN(nn.Module):
    def __init__(self, layer_info):
        super(CNN, self).__init__()
        self.layers = nn.ModuleList()
        pooling_sizes = []
        for subnetwork in layer_info:
            pooling_size = 0
            self.layers += [self.make_subnetwork(subnetwork)]
            for kernel in subnetwork:
                pooling_size += (-kernel + 1)
            pooling_sizes.append(pooling_size)
              
        if len(set(pooling_sizes)) != 1:
            raise "Different kernel sizes between subnetworks"
        pooling_size = pooling_sizes[0]
        num_subnetwork = len(layer_info)
        
        self.conv = nn.Conv2d(in_channels=128*num_subnetwork, out_channels=128*3, kernel_size=(1,1))
        self.batchnorm = nn.BatchNorm2d(num_features=128*3)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=(1000+pooling_size,1), stride=1)

    def make_subnetwork(self, subnetwork):
        subnetworks = []
        for i, kernel in enumerate(subnetwork):
            if i == 0:
                subnetworks.append(
                    nn.Sequential(
                        nn.Conv2d(in_channels=1, out_channels=128, kernel_size=(kernel, 20)),
                        nn.BatchNorm2d(num_features=128),
                        nn.ReLU(),
                        nn.Dropout(p=0.1)
                    )
                )
            else:
                subnetworks.append(
                    nn.Sequential(
                        nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(kernel, 1)),
                        nn.BatchNorm2d(num_features=128),
                        nn.ReLU(),
                        nn.Dropout(p=0.1)
                    )
                )
        return nn.Sequential(*subnetworks)

    def forward(self, x):
        xs = []
        for layer in self.layers:
            xs.append(layer(x))
        x = torch.cat(xs, dim=1)
        x = self.relu(self.batchnorm(self.conv(x)))
        x = self.pool(x)
        return x
    