"""
Pydantic Schemas for API Request Validation, Triage Contracts, and Clinical Chatbot.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


class ClinicalQuestionnaire(BaseModel):
    age: float = Field(..., ge=0, le=120, description="Patient age in years")
    sex: str = Field(..., description="Sex: Male, Female, or Unknown")
    lesion_location: str = Field(..., description="Anatomical site: head/neck, torso, extremities, etc.")
    evolution: str = Field(..., description="Recent changes: changed_recently, static, or uncertain")
    itching: bool = Field(False, description="Is itching present?")
    bleeding: bool = Field(False, description="Is bleeding present?")
    pain: bool = Field(False, description="Is pain present?")
    observed_color: str = Field("brown", description="User observed color: brown, black, red, pink, etc.")
    prior_allergies: bool = Field(False, description="Prior skin allergies")
    allergy_details: Optional[str] = Field("", description="Details of skin allergies")
    ongoing_medications: bool = Field(False, description="Ongoing medications")
    medication_details: Optional[str] = Field("", description="Details of ongoing medications")


class TopPrediction(BaseModel):
    class_code: str
    class_name: str
    probability: float
    percentage: str


class ImageQualityResult(BaseModel):
    is_valid: bool
    overall_score: float
    resolution: str
    blur_variance: float
    brightness_mean: float
    details: List[str]
    message: str


class ABCDEFeatures(BaseModel):
    asymmetry_score: float
    border_score: float
    color_score: float
    diameter_mm: float
    evolution_score: float
    evolution_text: str
    summary: str


class PredictionResponse(BaseModel):
    status: str
    model_architecture: str
    imaging_mode: str
    risk_level: str
    top_predicted_class: str
    top_class_human: str
    is_cancerous: bool
    cancer_status_label: str
    biopsy_required: bool
    biopsy_recommendation: str
    surgery_required: bool
    surgery_recommendation: str
    visit_urgency: str
    confidence: float
    confidence_percentage: str
    uncertainty: float
    uncertainty_percentage: str
    uncertainty_method: str
    all_7_predictions: List[TopPrediction]
    top_3_predictions: List[TopPrediction]
    image_quality: ImageQualityResult
    abcde_features: ABCDEFeatures
    reasoning: str
    recommendation: str
    healing_measures: List[str]
    explanation_image_b64: str
    roi_mask_image_b64: str
    disclaimer: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    triage_context: Optional[Dict[str, Any]] = None
    chat_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    reply: str
