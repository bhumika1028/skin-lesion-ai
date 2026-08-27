"""
Monte Carlo Dropout Bayesian Uncertainty Estimation Engine.
Performs T stochastic forward passes with active dropout to compute Bayesian predictive variance.
Inspired by DermaCalibra (Wang et al., 2026) and DUNEScan (Mazoure et al., 2022) cited in Mahin & Li (2026).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, Any, Tuple, List


def enable_dropout(model: nn.Module):
    """Enforces dropout layers to remain active during Monte Carlo inference."""
    for module in model.modules():
        if isinstance(module, (nn.Dropout, nn.Dropout2d, nn.Dropout3d)):
            module.train()


def run_monte_carlo_inference(
    model: nn.Module,
    img_tensor: torch.Tensor,
    age_norm: torch.Tensor,
    sex_idx: torch.Tensor,
    loc_idx: torch.Tensor,
    evo_idx: torch.Tensor,
    color_idx: torch.Tensor,
    symptoms: torch.Tensor,
    num_passes: int = 10
) -> Dict[str, Any]:
    """
    Executes T stochastic forward passes under Monte Carlo Dropout.
    Returns mean probabilities, predictive variance (uncertainty), and pass distribution.
    """
    model.eval()
    enable_dropout(model)  # Re-enable dropout at test time

    pass_probs = []

    for _ in range(num_passes):
        with torch.no_grad():
            outputs = model(img_tensor, age_norm, sex_idx, loc_idx, evo_idx, color_idx, symptoms)
            if 'probabilities' in outputs:
                probs = outputs['probabilities'][0]
            else:
                probs = F.softmax(outputs['logits'][0], dim=0)
            pass_probs.append(probs.cpu().numpy())

    pass_probs_arr = np.array(pass_probs)  # Shape: (T, K)

    # Calculate Mean Expected Probability across T passes
    mean_probs = np.mean(pass_probs_arr, axis=0)  # Shape: (K,)

    # Calculate Predictive Variance (Epistemic Uncertainty via MC Dropout)
    variance_per_class = np.var(pass_probs_arr, axis=0)  # Shape: (K,)
    total_mc_uncertainty = float(np.mean(variance_per_class))  # Overall MC variance metric
    normalized_mc_uncertainty = float(np.clip(total_mc_uncertainty * 15.0, 0.05, 0.95))  # Scale for UI

    return {
        'mean_probabilities': mean_probs,
        'variance_per_class': variance_per_class,
        'mc_uncertainty': total_mc_uncertainty,
        'normalized_uncertainty': normalized_mc_uncertainty,
        'pass_distribution': pass_probs_arr.tolist(),
        'num_passes': num_passes
    }
