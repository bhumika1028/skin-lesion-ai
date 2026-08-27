"""
Evidential Deep Learning (EDL) Head & Enhanced Clinical Risk Triage Engine.
Parameterizes Dirichlet distribution for uncertainty-aware skin lesion triage,
biopsy recommendation, surgical evaluation, and care protocols.
Inspired by Mahin & Li (2026).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, Tuple, List

from ml.models.swin_encoder import SwinVisualEncoder
from ml.models.metadata_encoder import MetadataEncoder
from ml.models.multimodal_fusion import CrossAttentionFusion


class EvidentialHead(nn.Module):
    """
    Evidential classification layer converting fused representations into Dirichlet evidence.
    """

    LESION_CLASSES = [
        'akiec',  # Actinic keratoses / intraepithelial carcinoma
        'bcc',    # Basal cell carcinoma
        'bkl',    # Benign keratosis-like lesions
        'df',     # Dermatofibroma
        'mel',    # Melanoma
        'nv',     # Melanocytic nevi
        'vasc'    # Vascular lesions
    ]

    MALIGNANT_CLASSES = {'mel', 'bcc'}
    PRECANCEROUS_CLASSES = {'akiec'}
    BENIGN_CLASSES = {'bkl', 'df', 'nv', 'vasc'}

    CLASS_NAMES_HUMAN = {
        'akiec': 'Actinic Keratosis / Intraepithelial Carcinoma (Pre-cancerous)',
        'bcc': 'Basal Cell Carcinoma (Malignant)',
        'bkl': 'Benign Keratosis-like Lesion (Benign)',
        'df': 'Dermatofibroma (Benign)',
        'mel': 'Melanoma (Malignant)',
        'nv': 'Melanocytic Nevus / Mole (Benign)',
        'vasc': 'Vascular Lesion (Benign)'
    }

    def __init__(self, feature_dim: int = 768, num_classes: int = 7):
        super(EvidentialHead, self).__init__()
        self.feature_dim = feature_dim
        self.num_classes = num_classes
        self.classifier = nn.Linear(feature_dim, num_classes)

    def forward(self, z_fused: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Forward pass for EDL.
        Returns:
            evidence (e_k): (B, K) >= 0
            alpha (alpha_k): (B, K) >= 1
            prob (p_hat): (B, K) normalized probabilities
            uncertainty (u): (B, 1) in [0, 1]
        """
        logits = self.classifier(z_fused)
        evidence = F.relu(logits)
        alpha = evidence + 1.0
        S = torch.sum(alpha, dim=1, keepdim=True)
        prob = alpha / S
        uncertainty = self.num_classes / S
        return evidence, alpha, prob, uncertainty


class SwinMultimodalEDL(nn.Module):
    """
    Full Unified Model Architecture combining:
    1. Swin Visual Encoder
    2. Clinical Metadata Encoder
    3. Cross-Attention Multimodal Fusion
    4. Dirichlet Evidential Deep Learning Head
    """

    def __init__(self, feature_dim: int = 768, num_classes: int = 7, pretrained: bool = True):
        super(SwinMultimodalEDL, self).__init__()
        self.feature_dim = feature_dim
        self.num_classes = num_classes

        self.visual_encoder = SwinVisualEncoder(feature_dim=feature_dim, pretrained=pretrained)
        self.metadata_encoder = MetadataEncoder(feature_dim=feature_dim)
        self.fusion_module = CrossAttentionFusion(feature_dim=feature_dim)
        self.evidential_head = EvidentialHead(feature_dim=feature_dim, num_classes=num_classes)

    def forward(
        self,
        images: torch.Tensor,
        age_norm: torch.Tensor,
        sex_idx: torch.Tensor,
        loc_idx: torch.Tensor,
        evo_idx: torch.Tensor,
        color_idx: torch.Tensor,
        symptoms: torch.Tensor
    ) -> Dict[str, torch.Tensor]:
        z_vis = self.visual_encoder(images)
        z_meta = self.metadata_encoder(age_norm, sex_idx, loc_idx, evo_idx, color_idx, symptoms)
        z_fused = self.fusion_module(z_vis, z_meta)
        evidence, alpha, prob, uncertainty = self.evidential_head(z_fused)

        return {
            'evidence': evidence,
            'alpha': alpha,
            'probabilities': prob,
            'uncertainty': uncertainty,
            'z_fused': z_fused,
            'z_vis': z_vis
        }

    @staticmethod
    def compute_triage_decision(
        prob_dict: Dict[str, float],
        uncertainty: float,
        image_quality_passed: bool = True,
        uncertainty_low_thresh: float = 0.25,
        uncertainty_high_thresh: float = 0.45,
        symptoms_info: Dict[str, bool] = None
    ) -> Dict[str, Any]:
        """
        Enhanced Risk Triage Engine assessing cancer status, biopsy necessity,
        surgical intervention needs, doctor visit urgency, and healing protocols.
        """
        top_class = max(prob_dict, key=prob_dict.get) if prob_dict else 'nv'
        top_prob = prob_dict.get(top_class, 0.0) if prob_dict else 0.0

        is_malignant = top_class in EvidentialHead.MALIGNANT_CLASSES
        is_precancerous = top_class in EvidentialHead.PRECANCEROUS_CLASSES
        is_cancerous = is_malignant or is_precancerous

        if is_malignant:
            cancer_status_label = "Malignant (Cancerous Pattern)"
        elif is_precancerous:
            cancer_status_label = "Pre-Cancerous (Actinic Keratosis)"
        else:
            cancer_status_label = "Benign (Non-Cancerous)"

        # Poor Quality Check
        if not image_quality_passed:
            return {
                'risk_level': 'EXPERT REVIEW RECOMMENDED',
                'top_predicted_class': top_class,
                'top_class_human': EvidentialHead.CLASS_NAMES_HUMAN.get(top_class, top_class),
                'is_cancerous': is_cancerous,
                'cancer_status_label': cancer_status_label,
                'biopsy_required': True,
                'biopsy_recommendation': 'Biopsy & Expert Evaluation Indicated due to poor image clarity.',
                'surgery_required': False,
                'surgery_recommendation': 'Clinical examination required before surgical planning.',
                'visit_urgency': 'RECOMMENDED (Within 1-2 Weeks)',
                'status_code': 'POOR_IMAGE_QUALITY',
                'reason': 'Uploaded image quality is insufficient (blur, illumination, or resolution issues). Reliable prediction cannot be made.',
                'recommendation': 'Please upload a clearer, well-lit dermoscopic image or consult a dermatologist for clinical examination.',
                'healing_measures': [
                    'Do not scratch, pick, or squeeze the lesion site.',
                    'Keep the skin clean and dry using gentle, fragrance-free soap.',
                    'Apply broad-spectrum SPF 50+ sunscreen when exposed to sunlight.',
                    'Schedule a face-to-face clinical skin check with a certified dermatologist.'
                ]
            }

        # Rule 1: High Uncertainty or Ambiguous
        if uncertainty > uncertainty_high_thresh:
            risk_level = 'EXPERT REVIEW RECOMMENDED'
            biopsy_req = True
            biopsy_rec = 'BIOPSY RECOMMENDED: Predictive uncertainty is high (u > 45%). Histopathological examination is required for definitive diagnosis.'
            surg_req = is_malignant
            surg_rec = 'Surgical excision or dermatologic evaluation indicated if biopsy confirms malignancy.'
            urgency = 'URGENT (Within 24-48 Hours)' if (is_cancerous or symptoms_info and symptoms_info.get('bleeding')) else 'RECOMMENDED (Within 1-2 Weeks)'
            reason = f'High predictive uncertainty (u = {uncertainty:.1%}). Available evidence is insufficient for autonomous classification.'
            rec = 'The lesion pattern or clinical presentation is ambiguous. Histopathological biopsy and dermatologist examination are strongly recommended.'
            healing = [
                'Avoid mechanical trauma, friction, or picking at the lesion.',
                'Keep the area clean using gentle dermatological washes.',
                'Protect from direct sunlight using physical barrier clothing or SPF 50+ sunscreen.',
                'Monitor for sudden growth, bleeding, or color changes while awaiting doctor consultation.'
            ]

        # Rule 2: Malignant / Suspicious OR Moderate Uncertainty
        elif is_cancerous or (uncertainty >= uncertainty_low_thresh):
            risk_level = 'SUSPICIOUS'
            biopsy_req = True
            biopsy_rec = 'BIOPSY STRONGLY INDICATED: Features consistent with suspicious/malignant tissue were detected.' if is_cancerous else 'BIOPSY RECOMMENDED: Moderate uncertainty warrants tissue sampling.'
            surg_req = top_class in {'mel', 'bcc'}
            surg_rec = 'Surgical Excision / Mohs Surgery evaluation required if histopathology confirms carcinoma.' if surg_req else 'Non-surgical dermatologic treatment or minor procedure may be indicated.'
            urgency = 'URGENT (Within 24-48 Hours)' if (top_class == 'mel' or (symptoms_info and symptoms_info.get('bleeding'))) else 'RECOMMENDED (Within 1-2 Weeks)'
            reason = f'Features associated with {cancer_status_label} identified (Confidence: {top_prob:.1%}).'
            rec = 'Prominent features of suspicious or malignant lesion morphology were detected. Immediate clinical assessment by a certified dermatologist is strongly advised.'
            healing = [
                'Apply sterile non-adherent dressing if the lesion is bleeding or oozing.',
                'Strictly avoid solar radiation exposure to the affected area; apply SPF 50+ zinc-based sunscreen.',
                'Do not apply harsh topical chemicals, acids, or unprescribed home remedies.',
                'Seek prompt dermatologist care for diagnostic punch/excisional biopsy.'
            ]

        # Rule 3: Low Risk (Benign)
        else:
            risk_level = 'LOW RISK'
            biopsy_req = False
            biopsy_rec = 'BIOPSY NOT CURRENTLY REQUIRED: Lesion exhibits a classic benign pattern with low model uncertainty.'
            surg_req = False
            surg_rec = 'No surgical operation required. Routine observation recommended.'
            urgency = 'ROUTINE (Annual Skin Checkup)'
            reason = f'Predicted as benign ({EvidentialHead.CLASS_NAMES_HUMAN.get(top_class, top_class)}) with strong evidence (Uncertainty: {uncertainty:.1%}).'
            rec = 'The lesion exhibits lower-risk benign characteristics. Continue routine self-monitoring. Consult a doctor if the lesion changes in size, shape, or color.'
            healing = [
                'Maintain routine daily moisturization with dermatological emollients.',
                'Apply broad-spectrum SPF 30+ or SPF 50+ sunscreen daily.',
                'Perform monthly self-skin exams checking for the ABCDE signs of melanoma.',
                'Schedule routine annual dermatological checkups.'
            ]

        return {
            'risk_level': 'LOW RISK' if risk_level == 'LOW RISK' else ('SUSPICIOUS' if risk_level == 'SUSPICIOUS' else 'EXPERT REVIEW RECOMMENDED'),
            'top_predicted_class': top_class,
            'top_class_human': EvidentialHead.CLASS_NAMES_HUMAN.get(top_class, top_class),
            'is_cancerous': is_cancerous,
            'cancer_status_label': cancer_status_label,
            'biopsy_required': biopsy_req,
            'biopsy_recommendation': biopsy_rec,
            'surgery_required': surg_req,
            'surgery_recommendation': surg_rec,
            'visit_urgency': urgency,
            'top_confidence': top_prob,
            'uncertainty_score': uncertainty,
            'reason': reason,
            'recommendation': rec,
            'healing_measures': healing
        }


def edl_mse_loss(alpha: torch.Tensor, target_onehot: torch.Tensor, epoch_num: int, max_epochs: int) -> torch.Tensor:
    S = torch.sum(alpha, dim=1, keepdim=True)
    prob = alpha / S
    err = torch.sum((target_onehot - prob) ** 2, dim=1, keepdim=True)
    var = torch.sum(alpha * (S - alpha) / (S * S * (S + 1.0)), dim=1, keepdim=True)
    loss_err = torch.mean(err + var)

    alpha_til = target_onehot + (1.0 - target_onehot) * alpha
    S_til = torch.sum(alpha_til, dim=1, keepdim=True)
    
    kl_first = torch.lgamma(S_til) - torch.sum(torch.lgamma(alpha_til), dim=1, keepdim=True)
    kl_second = torch.sum((alpha_til - 1.0) * (torch.digamma(alpha_til) - torch.digamma(S_til)), dim=1, keepdim=True)
    loss_kl = torch.mean(kl_first + kl_second)

    anneal_coef = min(1.0, float(epoch_num) / max(1, max_epochs // 2))
    return loss_err + anneal_coef * loss_kl
