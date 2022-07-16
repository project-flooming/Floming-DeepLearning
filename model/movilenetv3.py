import torch 
import torch.nn as nn
import torchvision.models as models

class MobileNetV3(nn.Module):
    def __init__(
        self,
        in_dim=3,
        num_classes=100,
        pre_trained=True,
    ):
        super(MobileNetV3, self).__init__()
        model = models.mobilenet_v3_large(pretrained=pre_trained)
        self.features = model.features
        self.avgpool = model.avgpool
        self.classifier = nn.Sequential(
            model.classifier[0],
            model.classifier[1],
            model.classifier[2],
            nn.Linear(1280, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size()[0], -1)
        x = self.classifier(x)
        return x