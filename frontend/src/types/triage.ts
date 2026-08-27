export interface ClinicalFormData {
  age: number;
  sex: 'Male' | 'Female' | 'Unknown';
  lesion_location: string;
  evolution: 'changed_recently' | 'static' | 'uncertain';
  itching: boolean;
  bleeding: boolean;
  pain: boolean;
  observed_color: string;
  prior_allergies: boolean;
  allergy_details: string;
  ongoing_medications: boolean;
  medication_details: string;
  model_architecture: 'swin_edl' | 'monte_carlo' | 'mobile_vit';
  imaging_mode: 'dermoscopic' | 'smartphone';
  fitzpatrick_scale: string;
}

export interface TopPrediction {
  class_code: string;
  class_name: string;
  probability: number;
  percentage: string;
}

export interface ImageQualityResult {
  is_valid: boolean;
  overall_score: number;
  resolution: string;
  blur_variance: number;
  brightness_mean: number;
  details: string[];
  message: string;
}

export interface ABCDEFeatures {
  asymmetry_score: number;
  border_score: number;
  color_score: number;
  diameter_mm: number;
  evolution_score: number;
  evolution_text: string;
  summary: string;
}

export interface PredictionResponse {
  status: string;
  model_architecture: string;
  imaging_mode: string;
  risk_level: 'LOW RISK' | 'SUSPICIOUS' | 'EXPERT REVIEW RECOMMENDED';
  top_predicted_class: string;
  top_class_human: string;
  is_cancerous: boolean;
  cancer_status_label: string;
  biopsy_required: boolean;
  biopsy_recommendation: string;
  surgery_required: boolean;
  surgery_recommendation: string;
  visit_urgency: string;
  confidence: number;
  confidence_percentage: string;
  uncertainty: number;
  uncertainty_percentage: string;
  uncertainty_method: string;
  all_7_predictions: TopPrediction[];
  top_3_predictions: TopPrediction[];
  image_quality: ImageQualityResult;
  abcde_features: ABCDEFeatures;
  reasoning: string;
  recommendation: string;
  healing_measures: string[];
  explanation_image_b64: string;
  roi_mask_image_b64: string;
  disclaimer: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ModelBenchmark {
  model_name: string;
  accuracy: number;
  balanced_accuracy: number;
  precision: number;
  recall_sensitivity: number;
  specificity: number;
  f1_score: number;
  macro_f1: number;
  roc_auc: number;
  ece: number;
  is_proposed: boolean;
}

export interface ResearchMetricsResponse {
  status: string;
  benchmarks: {
    models: ModelBenchmark[];
    dataset_summary: {
      total_samples: number;
      classes: Record<string, number>;
    };
  };
  ablation: {
    ablation_experiments: Array<{
      case: string;
      accuracy: number;
      recall: number;
      auc: number;
      ece: number;
    }>;
  };
}
