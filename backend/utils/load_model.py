# load the 07_effnetb2_data_20_percent_10_epochs
import torch
from torchvision.models import efficientnet_b2, EfficientNet_B2_Weights
from torch import nn

def load_model():
    """Load the effientnetB2 model with 92 percent accuracy"""   
    weights = torch.load("models/07_effnetb2_data_20_percent_10_epochs.pt")
    model = efficientnet_b2()
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features=1408, out_features=3, bias=True)
    )
    model.load_state_dict(weights)
    return model
    


