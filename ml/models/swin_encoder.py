"""
Swin Transformer Visual Feature Extractor Module.
Hierarchical Vision Transformer utilizing Shifted Window (SW-MSA) self-attention
to capture fine-grained textural irregularities and global morphological structures.
Inspired by Mahin & Li (2026).
"""

import torch
import torch.nn as nn
try:
    import timm
    HAS_TIMM = True
except ImportError:
    HAS_TIMM = False


class SwinVisualEncoder(nn.Module):
    """
    Swin Transformer backbone for dermoscopic visual feature extraction.
    Outputs a feature vector of dimension feature_dim (default: 768).
    """

    def __init__(self, model_name: str = 'swin_tiny_patch4_window7_224', feature_dim: int = 768, pretrained: bool = True):
        super(SwinVisualEncoder, self).__init__()
        self.model_name = model_name
        self.feature_dim = feature_dim
        
        if HAS_TIMM:
            try:
                # Load pretrained Swin-Tiny model from timm
                self.backbone = timm.create_model(
                    model_name,
                    pretrained=pretrained,
                    num_classes=0  # Remove classification head to get feature embedding
                )
                in_features = self.backbone.num_features
                self.proj = nn.Sequential(
                    nn.Linear(in_features, feature_dim),
                    nn.BatchNorm1d(feature_dim),
                    nn.GELU()
                )
                self.use_fallback = False
            except Exception as e:
                print(f"[Warning] timm model creation failed: {e}. Using standalone CNN/ViT backbone fallback.")
                self._build_fallback(feature_dim)
        else:
            self._build_fallback(feature_dim)

    def _build_fallback(self, feature_dim: int):
        """Fallback lightweight convolutional-transformer module if timm weights unavailable."""
        self.use_fallback = True
        self.backbone = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(256, 512, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten()
        )
        self.proj = nn.Sequential(
            nn.Linear(512, feature_dim),
            nn.BatchNorm1d(feature_dim),
            nn.GELU()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for visual pipeline.
        Input x: (B, 3, 224, 224)
        Output: (B, feature_dim)
        """
        features = self.backbone(x)
        if len(features.shape) > 2:
            features = torch.flatten(features, 1)
        z_vis = self.proj(features)
        return z_vis


if __name__ == '__main__':
    # Sanity check
    dummy_input = torch.randn(2, 3, 224, 224)
    model = SwinVisualEncoder(pretrained=False)
    out = model(dummy_input)
    print(f"SwinVisualEncoder Output Shape: {out.shape}")
