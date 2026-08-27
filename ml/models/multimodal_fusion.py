"""
Attention-Based Multimodal Fusion Module.
Performs cross-attention between Swin Transformer visual features (Keys/Values)
and Clinical Metadata representation (Query).
Inspired by Mahin & Li (2026).
"""

import math
import torch
import torch.nn as nn


class CrossAttentionFusion(nn.Module):
    """
    Cross-Attention layer fusing heterogeneous visual and clinical metadata embeddings.
    """

    def __init__(self, feature_dim: int = 768, num_heads: int = 8):
        super(CrossAttentionFusion, self).__init__()
        self.feature_dim = feature_dim
        self.num_heads = num_heads
        self.head_dim = feature_dim // num_heads

        assert self.head_dim * num_heads == feature_dim, "feature_dim must be divisible by num_heads"

        self.w_q = nn.Linear(feature_dim, feature_dim, bias=False)
        self.w_k = nn.Linear(feature_dim, feature_dim, bias=False)
        self.w_v = nn.Linear(feature_dim, feature_dim, bias=False)

        self.out_proj = nn.Linear(feature_dim, feature_dim)
        self.layer_norm = nn.LayerNorm(feature_dim)
        self.dropout = nn.Dropout(0.1)

    def forward(self, z_vis: torch.Tensor, z_meta: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for Cross-Attention Fusion.
        z_vis: (B, feature_dim)
        z_meta: (B, feature_dim)
        Output: z_fused (B, feature_dim)
        """
        B = z_vis.shape[0]

        # Project Query (Metadata) and Key/Value (Visual)
        Q = self.w_q(z_meta).view(B, 1, self.num_heads, self.head_dim).transpose(1, 2)  # (B, num_heads, 1, head_dim)
        K = self.w_k(z_vis).view(B, 1, self.num_heads, self.head_dim).transpose(1, 2)   # (B, num_heads, 1, head_dim)
        V = self.w_v(z_vis).view(B, 1, self.num_heads, self.head_dim).transpose(1, 2)   # (B, num_heads, 1, head_dim)

        # Scaled Dot-Product Attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)        # (B, num_heads, 1, 1)
        attn_weights = torch.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)

        context = torch.matmul(attn_weights, V)                                        # (B, num_heads, 1, head_dim)
        context = context.transpose(1, 2).contiguous().view(B, self.feature_dim)        # (B, feature_dim)

        attn_out = self.out_proj(context)
        
        # Residual connection & LayerNorm
        z_fused = self.layer_norm(z_vis + attn_out)
        return z_fused


if __name__ == '__main__':
    fusion = CrossAttentionFusion(feature_dim=768, num_heads=8)
    z_vis = torch.randn(2, 768)
    z_meta = torch.randn(2, 768)
    out = fusion(z_vis, z_meta)
    print(f"CrossAttentionFusion Output Shape: {out.shape}")
