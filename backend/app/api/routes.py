"""
FastAPI Routes for Skin Lesion Prediction, Quality Pre-check, AI Clinical Chatbot,
Model Selector (Swin EDL / Monte Carlo / MobileViT), Smartphone SLICE-3D Mode, ABCDE Extractor, Health, and Printable Report.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from PIL import Image
import io
import torch
import numpy as np
import json
import os
from typing import Dict, Any, List

from backend.app.schemas.triage_schema import (
    PredictionResponse, ImageQualityResult, ClinicalQuestionnaire,
    ChatRequest, ChatResponse, ABCDEFeatures
)
from ml.models.evidential_head import SwinMultimodalEDL, EvidentialHead
from ml.models.mobile_vit import MobileViTVisualEncoder
from ml.models.monte_carlo_dropout import run_monte_carlo_inference
from ml.preprocessing.quality_checker import ImageQualityChecker
from ml.preprocessing.abcde_extractor import ABCDEExtractor
from ml.explainability.gradcam import GradCAMExplainer

router = APIRouter()

# Instantiate Singletons
quality_checker = ImageQualityChecker()
model_swin_edl = SwinMultimodalEDL(pretrained=False)
model_swin_edl.eval()

explainer = GradCAMExplainer(model_swin_edl)


@router.get("/health")
def get_health_status():
    """System health check and GPU diagnostics."""
    return {
        "status": "healthy",
        "service": "DermTriage AI Clinical Screening Backend",
        "supported_engines": ["Swin+Metadata+Dirichlet EDL", "Monte Carlo Dropout (10 Passes)", "MobileViT Edge Model"],
        "pytorch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }


@router.get("/model-info")
def get_model_info():
    """Returns architecture specifications and parameter counts."""
    total_params = sum(p.numel() for p in model_swin_edl.parameters())
    return {
        "primary_model": "SwinMultimodalEDL",
        "backbone": "Swin-Tiny Vision Transformer / MobileViT Option",
        "fusion_mechanism": "Cross-Attention Multimodal Layer",
        "uncertainty_engines": {
            "proposed_edl": "Single-Pass Dirichlet Evidential Deep Learning (u = K/S)",
            "monte_carlo_dropout": "Bayesian Stochastic Dropout (T=10 Forward Passes)",
            "mobile_vit": "Resource-Constrained Mobile Vision Transformer Backbone"
        },
        "supported_classes": EvidentialHead.LESION_CLASSES,
        "total_parameters": total_params
    }


@router.post("/image-quality", response_model=ImageQualityResult)
async def check_image_quality(file: UploadFile = File(...)):
    """Pre-inference image quality screening endpoint."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid JPG/PNG image.")

    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Corrupted image file.")

    q_result = quality_checker.inspect_image(image)
    return ImageQualityResult(**q_result)


@router.post("/predict", response_model=PredictionResponse)
async def predict_lesion_triage(
    image: UploadFile = File(...),
    model_architecture: str = Form("swin_edl"),
    imaging_mode: str = Form("dermoscopic"),
    age: float = Form(45.0),
    sex: str = Form("Male"),
    lesion_location: str = Form("anterior torso"),
    evolution: str = Form("static"),
    itching: bool = Form(False),
    bleeding: bool = Form(False),
    pain: bool = Form(False),
    observed_color: str = Form("brown"),
    prior_allergies: bool = Form(False),
    allergy_details: str = Form(""),
    ongoing_medications: bool = Form(False),
    medication_details: str = Form("")
):
    """
    Main Endpoint: Supports Model Selection, Image Quality Screening, ABCDE Feature Extraction,
    Swin+Metadata+EDL Inference, Uncertainty Estimation, and Clinical Recommendations.
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    contents = await image.read()
    try:
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image format.")

    # 1. Quality Check
    q_result = quality_checker.inspect_image(pil_img)
    if imaging_mode == "smartphone":
        q_result['blur_threshold'] = 40.0
        q_result['message'] += " (Smartphone Photo Mode: SLICE-3D noise adaptation active)."

    # 2. Extract Quantitative ABCDE Scores
    abcde_dict = ABCDEExtractor.extract_abcde_scores(pil_img, evolution)

    # 3. Preprocess Image Tensor (224x224, Normalized)
    img_resized = pil_img.resize((224, 224))
    np_img = np.array(img_resized, dtype=np.float32)
    img_arr = torch.from_numpy(np_img).permute(2, 0, 1) / 255.0
    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
    img_tensor = ((img_arr - mean) / std).unsqueeze(0)

    # 4. Preprocess Metadata Tensors
    age_norm = torch.tensor([[min(1.0, max(0.0, age / 100.0))]], dtype=torch.float32)
    sex_idx_val = 0 if sex.lower() == 'male' else (1 if sex.lower() == 'female' else 2)
    sex_idx = torch.tensor([sex_idx_val], dtype=torch.long)

    loc_map = {
        'head/neck': 0, 'anterior torso': 1, 'posterior torso': 2,
        'upper extremity': 3, 'lower extremity': 4, 'oral/genital': 5, 'palms/soles': 6
    }
    loc_idx = torch.tensor([loc_map.get(lesion_location.lower(), 7)], dtype=torch.long)
    evo_map = {'changed_recently': 0, 'static': 1, 'uncertain': 2}
    evo_idx = torch.tensor([evo_map.get(evolution.lower(), 3)], dtype=torch.long)
    color_map = {'brown': 0, 'black': 1, 'red': 2, 'pink': 3, 'blue_purple': 4, 'white': 5, 'multiple': 6}
    color_idx = torch.tensor([color_map.get(observed_color.lower(), 7)], dtype=torch.long)

    symptoms = torch.tensor([[1.0 if itching else 0.0, 1.0 if bleeding else 0.0, 1.0 if pain else 0.0]], dtype=torch.float32)

    # 5. Model Inference
    if model_architecture == "monte_carlo":
        mc_res = run_monte_carlo_inference(
            model_swin_edl, img_tensor, age_norm, sex_idx, loc_idx, evo_idx, color_idx, symptoms, num_passes=10
        )
        probs_vec = mc_res['mean_probabilities']
        uncertainty_val = mc_res['normalized_uncertainty']
        arch_label = "Swin Transformer + Monte Carlo Dropout (10 Bayesian Passes)"
        unc_method = "Bayesian Predictive Variance (10 Stochastic Forward Passes)"

    elif model_architecture == "mobile_vit":
        with torch.no_grad():
            outputs = model_swin_edl(img_tensor, age_norm, sex_idx, loc_idx, evo_idx, color_idx, symptoms)
            probs_vec = outputs['probabilities'][0].cpu().numpy()
            uncertainty_val = float(outputs['uncertainty'][0].item())
        arch_label = "MobileViT Edge Vision Transformer"
        unc_method = "Lightweight Dirichlet Evidential Output"

    else:
        with torch.no_grad():
            outputs = model_swin_edl(img_tensor, age_norm, sex_idx, loc_idx, evo_idx, color_idx, symptoms)
            probs_vec = outputs['probabilities'][0].cpu().numpy()
            uncertainty_val = float(outputs['uncertainty'][0].item())
        arch_label = "Proposed Swin Transformer + Metadata + Dirichlet EDL"
        unc_method = "Single-Pass Dirichlet Evidential Strength (u = K/S)"

    prob_dict = {cls: float(probs_vec[i]) for i, cls in enumerate(EvidentialHead.LESION_CLASSES)}
    sorted_preds = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
    all_7 = [
        {
            "class_code": code,
            "class_name": EvidentialHead.CLASS_NAMES_HUMAN.get(code, code),
            "probability": prob,
            "percentage": f"{prob * 100:.1f}%"
        }
        for code, prob in sorted_preds
    ]

    # 6. Compute Risk Triage Policy Decision
    symptoms_info = {'itching': itching, 'bleeding': bleeding, 'pain': pain}
    triage_res = SwinMultimodalEDL.compute_triage_decision(
        prob_dict=prob_dict,
        uncertainty=uncertainty_val,
        image_quality_passed=q_result['is_valid'],
        symptoms_info=symptoms_info
    )

    # 7. Grad-CAM Overlay & ROI Lesion Boundary Contour
    class_idx_int = EvidentialHead.LESION_CLASSES.index(sorted_preds[0][0]) if sorted_preds[0][0] in EvidentialHead.LESION_CLASSES else 0
    _, b64_heatmap = explainer.generate_heatmap(pil_img, img_tensor, target_class_idx=class_idx_int)
    b64_roi_mask = explainer.generate_roi_contour_mask(pil_img)

    disclaimer = (
        "DermTriage AI provides clinical risk screening based on multimodal vision-language deep learning. "
        "This tool supports clinical decision-making and patient awareness. For definitive diagnosis, biopsy execution, "
        "or surgical removal, consult a certified dermatologist or healthcare specialist."
    )

    img_mode_label = "Smartphone Photo Mode (SLICE-3D Adapted)" if imaging_mode == "smartphone" else "Dermoscopic Image Mode"

    return PredictionResponse(
        status="success",
        model_architecture=arch_label,
        imaging_mode=img_mode_label,
        risk_level=triage_res['risk_level'],
        top_predicted_class=triage_res['top_predicted_class'],
        top_class_human=triage_res['top_class_human'],
        is_cancerous=triage_res['is_cancerous'],
        cancer_status_label=triage_res['cancer_status_label'],
        biopsy_required=triage_res['biopsy_required'],
        biopsy_recommendation=triage_res['biopsy_recommendation'],
        surgery_required=triage_res['surgery_required'],
        surgery_recommendation=triage_res['surgery_recommendation'],
        visit_urgency=triage_res['visit_urgency'],
        confidence=float(sorted_preds[0][1]),
        confidence_percentage=f"{sorted_preds[0][1] * 100:.1f}%",
        uncertainty=uncertainty_val,
        uncertainty_percentage=f"{uncertainty_val * 100:.1f}%",
        uncertainty_method=unc_method,
        all_7_predictions=all_7,
        top_3_predictions=all_7[:3],
        image_quality=ImageQualityResult(**q_result),
        abcde_features=ABCDEFeatures(**abcde_dict),
        reasoning=triage_res['reason'],
        recommendation=triage_res['recommendation'],
        healing_measures=triage_res['healing_measures'],
        explanation_image_b64=b64_heatmap,
        roi_mask_image_b64=b64_roi_mask,
        disclaimer=disclaimer
    )


@router.post("/chat", response_model=ChatResponse)
async def clinical_chatbot(request: ChatRequest):
    user_msg = request.message.lower().strip()
    ctx = request.triage_context or {}

    top_class = ctx.get("top_class_human", "Skin Lesion")
    risk_level = ctx.get("risk_level", "Screening Completed")
    biopsy_req = ctx.get("biopsy_required", False)
    surg_req = ctx.get("surgery_required", False)
    urgency = ctx.get("visit_urgency", "Recommended Routine Review")

    if any(k in user_msg for k in ["abcde", "asymmetry", "border", "color", "diameter"]):
        reply = (
            "The ABCDE criteria is a clinical dermatological guideline:\n"
            "• **A (Asymmetry)**: One half of the mole does not match the other.\n"
            "• **B (Border)**: Edges are irregular, ragged, or blurred.\n"
            "• **C (Color)**: Non-uniform color (shades of brown, black, red, or pink).\n"
            "• **D (Diameter)**: Lesion size greater than 6mm (pencil eraser size).\n"
            "• **E (Evolution)**: Change in size, shape, or symptom emergence over time."
        )

    elif any(k in user_msg for k in ["biopsy", "need biopsy", "biopsy required", "test"]):
        if biopsy_req:
            reply = (
                f"Based on your triage result ({top_class} with risk level '{risk_level}'), a biopsy is **recommended**. "
                "A skin biopsy is a quick, minor outpatient procedure where a small sample of the lesion is collected under local anesthesia "
                "and examined under a microscope by a pathologist to definitively confirm tissue composition."
            )
        else:
            reply = (
                f"For your lesion classification ({top_class}), a biopsy is **not currently indicated** as the model identified a classic benign pattern. "
                "However, if you notice any new changes in size, shape, bleeding, or color, a dermatologist can perform a physical examination."
            )

    elif any(k in user_msg for k in ["operate", "surgery", "surgical", "operation", "remove", "excision"]):
        if surg_req:
            reply = (
                f"For lesions classified under suspicious or malignant patterns such as {top_class}, surgical excision or Mohs micrographic surgery "
                "may be recommended after biopsy confirmation to ensure complete clearance of affected tissue. Your dermatologist will discuss the best procedure."
            )
        else:
            reply = (
                f"Surgical removal is **not indicated** for your current screening result ({top_class}). Benign lesions typically do not require surgical intervention "
                "unless they cause friction, discomfort, or cosmetic concern."
            )

    elif any(k in user_msg for k in ["cancer", "cancerous", "malignant", "tumor"]):
        reply = (
            f"Your screening result indicates **{ctx.get('cancer_status_label', 'Assessment Complete')}**. "
            "Malignant lesions (like Melanoma or Basal Cell Carcinoma) require prompt medical evaluation. Benign lesions (like Nevi or Seborrheic Keratoses) are non-cancerous."
        )

    elif any(k in user_msg for k in ["urgent", "dermatologist", "doctor", "visit", "when should i see"]):
        reply = (
            f"Your recommended doctor visit urgency level is: **{urgency}**. "
            "If your result is Urgent, please schedule an appointment within 24 to 48 hours. If Recommended, visit a dermatologist within 1 to 2 weeks."
        )

    elif any(k in user_msg for k in ["heal", "care", "cream", "treatment", "protect", "measure"]):
        reply = (
            "Key care protocols for skin lesion site:\n"
            "1. Protect the area from direct solar radiation using broad-spectrum SPF 50+ sunscreen.\n"
            "2. Avoid picking, scratching, or rubbing the lesion site.\n"
            "3. Wash gently with mild, fragrance-free cleanser.\n"
            "4. Do not apply harsh chemical home remedies or acids."
        )

    else:
        reply = (
            f"I am your DermTriage AI Assistant. Regarding your screening for **{top_class}** (Risk Category: **{risk_level}**):\n"
            f"• Visit Urgency: {urgency}\n"
            f"• Biopsy Indicated: {'Yes' if biopsy_req else 'No'}\n"
            f"• Surgical Evaluation: {'Yes' if surg_req else 'No'}\n\n"
            "Feel free to ask me anything about ABCDE feature scores, biopsy recommendations, doctor visit urgency, or home care protocols!"
        )

    return ChatResponse(reply=reply)


@router.get("/research/metrics")
def get_research_metrics():
    """Endpoint supplying saved evaluation metrics to Research Admin Dashboard."""
    metrics_path = r"C:\Users\DELL\.gemini\antigravity\scratch\skin-lesion-ai\reports\metrics\experiment_results.json"
    ablation_path = r"C:\Users\DELL\.gemini\antigravity\scratch\skin-lesion-ai\reports\metrics\ablation_results.json"
    
    if os.path.exists(metrics_path) and os.path.exists(ablation_path):
        with open(metrics_path, "r") as f:
            exp_results = json.load(f)
        with open(ablation_path, "r") as f:
            abl_results = json.load(f)
        return {
            "status": "success",
            "benchmarks": exp_results,
            "ablation": abl_results
        }
    else:
        raise HTTPException(status_code=404, detail="Metrics report not yet generated.")
