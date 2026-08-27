"""
Clinical Metadata Encoder Module.
Encodes patient demographics and lesion questionnaire variables (Age, Sex, Location, Evolution, Symptoms, Color)
into a dense embedding vector matching the visual feature dimension.
Inspired by Mahin & Li (2026).
"""

import torch
import torch.nn as nn
from typing import Dict, Any


class MetadataEncoder(nn.Module):
    """
    MLP & Categorical Embedding Encoder for Clinical Metadata.
    """

    SEX_CATEGORIES = ['Male', 'Female', 'Unknown']
    LOCATION_CATEGORIES = [
        'head/neck', 'anterior torso', 'posterior torso', 
        'upper extremity', 'lower extremity', 'oral/genital', 'palms/soles', 'Unknown'
    ]
    EVOLUTION_CATEGORIES = ['changed_recently', 'static', 'uncertain', 'Unknown']
    COLOR_CATEGORIES = ['brown', 'black', 'red', 'pink', 'blue_purple', 'white', 'multiple', 'not_sure']

    def __init__(self, feature_dim: int = 768):
        super(MetadataEncoder, self).__init__()
        self.feature_dim = feature_dim
        
        # Categorical Embeddings
        self.sex_embed = nn.Embedding(num_embeddings=len(self.SEX_CATEGORIES) + 1, embedding_dim=16)
        self.loc_embed = nn.Embedding(num_embeddings=len(self.LOCATION_CATEGORIES) + 1, embedding_dim=32)
        self.evo_embed = nn.Embedding(num_embeddings=len(self.EVOLUTION_CATEGORIES) + 1, embedding_dim=16)
        self.color_embed = nn.Embedding(num_embeddings=len(self.COLOR_CATEGORIES) + 1, embedding_dim=16)

        # Input dimension: 
        # Age (1) + Sex_embed (16) + Loc_embed (32) + Evo_embed (16) + Color_embed (16) + Symptoms (3: itch, bleed, pain) = 85
        total_meta_dim = 1 + 16 + 32 + 16 + 16 + 3

        self.mlp = nn.Sequential(
            nn.Linear(total_meta_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(256, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(512, feature_dim),
            nn.BatchNorm1d(feature_dim),
            nn.GELU()
        )

    def forward(
        self, 
        age_norm: torch.Tensor,       # (B, 1) float in [0, 1]
        sex_idx: torch.Tensor,        # (B,) int
        loc_idx: torch.Tensor,        # (B,) int
        evo_idx: torch.Tensor,        # (B,) int
        color_idx: torch.Tensor,      # (B,) int
        symptoms: torch.Tensor        # (B, 3) float tensor [itch, bleed, pain]
    ) -> torch.Tensor:
        """
        Encodes clinical metadata payload into dense z_meta vector of size (B, feature_dim).
        """
        e_sex = self.sex_embed(sex_idx)
        e_loc = self.loc_embed(loc_idx)
        e_evo = self.evo_embed(evo_idx)
        e_color = self.color_embed(color_idx)

        concat_meta = torch.cat([age_norm, e_sex, e_loc, e_evo, e_color, symptoms], dim=1)
        z_meta = self.mlp(concat_meta)
        return z_meta


if __name__ == '__main__':
    batch_size = 2
    encoder = MetadataEncoder(feature_dim=768)
    age = torch.tensor([[0.45], [0.65]])
    sex = torch.tensor([0, 1])
    loc = torch.tensor([1, 3])
    evo = torch.tensor([0, 1])
    color = torch.tensor([2, 0])
    symptoms = torch.tensor([[1.0, 0.0, 0.0], [0.0, 1.0, 1.0]])
    
    out = encoder(age, sex, loc, evo, color, symptoms)
    print(f"MetadataEncoder Output Shape: {out.shape}")
