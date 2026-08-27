"""
MobileViT Visual Feature Extractor Module.
Lightweight Mobile Vision Transformer combining MobilenetV3 spatial convolutions
with ViT global self-attention for edge/mobile dermoscopic triage.
Inspired by MobileViT literature & Mahin & Li (2026).
"""

import torch
import torch.nn as nn
try:
    import timm
    HAS_TIMM = True
except ImportError:
    HAS_TIMM = False


class MobileViTVisualEncoder(nn.Module):
    """
    MobileViT feature extractor for resource-constrained edge deployments.
    """

    def __init__(self, model_name: str = 'mobilevit_s', feature_dim: int = 768, pretrained: bool = True):
        super(MobileViTVisualEncoder, self).__init__()
        self.feature_dim = feature_dim
        
        if HAS_TIMM:
            try:
                self.backbone = timm.create_model(
                    model_name,
                    pretrained=pretrained,
                    num_classes=0
                )
                in_features = self.backbone.num_features
                self.proj = nn.Sequential(
                    nn.Linear(in_features, feature_dim),
                    nn.BatchNorm1d(feature_dim),
                    nn.GELU()
                )
                self.use_fallback = False
            except Exception as e:
                print(f"[Warning] MobileViT creation failed: {e}. Using MobileNet fallback.")
                self._build_fallback(feature_dim)
        else:
            self._build_fallback(feature_dim)

    def _build_fallback(self, feature_dim: int):
        self.use_fallback = True
        self.backbone = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.SiLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.SiLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.SiLU(),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.SiLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten()
        )
        self.proj = nn.Sequential(
            nn.Linear(256, feature_dim),
            nn.BatchNorm1d(feature_dim),
            nn.GELU()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.backbone(x)
        if len(features.shape) > 2:
            features = torch.flatten(features, 1)
        return self.proj(features)


if __name__ == '__main__':
    dummy_input = torch.randn(2, 3, 224, 224)
    model = MobileViTVisualEncoder(pretrained=False)
    out = model(dummy_input)
    print("MobileViT Output Shape:", out.shape)
