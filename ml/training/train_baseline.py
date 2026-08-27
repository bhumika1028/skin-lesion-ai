"""
PyTorch Baseline Model Training Script (ResNet50 & EfficientNet-B0).
Used for comparative evaluation against the proposed Swin+Metadata+EDL model.
"""

import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models


class BaselineSkinClassifier(nn.Module):
    """
    Standard Vision Baseline (ResNet50 / EfficientNet) with Softmax decision layer.
    """

    def __init__(self, backbone_type: str = "resnet50", num_classes: int = 7):
        super(BaselineSkinClassifier, self).__init__()
        self.backbone_type = backbone_type
        
        if backbone_type == "resnet50":
            self.backbone = models.resnet50(pretrained=True)
            in_features = self.backbone.fc.in_features
            self.backbone.fc = nn.Linear(in_features, num_classes)
        else:
            self.backbone = models.efficientnet_b0(pretrained=True)
            in_features = self.backbone.classifier[1].in_features
            self.backbone.classifier[1] = nn.Linear(in_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        logits = self.backbone(x)
        probs = torch.softmax(logits, dim=1)
        return probs


if __name__ == '__main__':
    model = BaselineSkinClassifier(backbone_type="resnet50")
    dummy_input = torch.randn(2, 3, 224, 224)
    probs = model(dummy_input)
    print(f"ResNet50 Baseline Probabilities Shape: {probs.shape}")
