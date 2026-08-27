"""
Root Training Entrypoint for Skin Lesion Detection & Risk Triage Model.
Runs the PyTorch Swin Transformer + Clinical Metadata + Evidential Deep Learning (EDL) training pipeline.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.training.train_multimodal_edl import train_model

if __name__ == '__main__':
    print("==================================================================")
    print("  Skin Lesion AI - Model Training Pipeline (Swin + Metadata + EDL)")
    print("==================================================================")
    train_model(epochs=5, batch_size=8, learning_rate=1e-4)
