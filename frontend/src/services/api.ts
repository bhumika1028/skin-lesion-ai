import axios from 'axios';
import { ClinicalFormData, PredictionResponse, ImageQualityResult, ResearchMetricsResponse } from '../types/triage';

const API_BASE = '/api';

export const submitTriageAnalysis = async (
  imageFile: File,
  formData: ClinicalFormData
): Promise<PredictionResponse> => {
  const payload = new FormData();
  payload.append('image', imageFile);
  payload.append('model_architecture', formData.model_architecture);
  payload.append('imaging_mode', formData.imaging_mode);
  payload.append('age', formData.age.toString());
  payload.append('sex', formData.sex);
  payload.append('lesion_location', formData.lesion_location);
  payload.append('evolution', formData.evolution);
  payload.append('itching', formData.itching.toString());
  payload.append('bleeding', formData.bleeding.toString());
  payload.append('pain', formData.pain.toString());
  payload.append('observed_color', formData.observed_color);
  payload.append('prior_allergies', formData.prior_allergies.toString());
  payload.append('allergy_details', formData.allergy_details);
  payload.append('ongoing_medications', formData.ongoing_medications.toString());
  payload.append('medication_details', formData.medication_details);

  const response = await axios.post<PredictionResponse>(`${API_BASE}/predict`, payload, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const checkImageQuality = async (imageFile: File): Promise<ImageQualityResult> => {
  const payload = new FormData();
  payload.append('file', imageFile);
  const response = await axios.post<ImageQualityResult>(`${API_BASE}/image-quality`, payload, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const sendChatMessage = async (
  message: string,
  triageContext?: any
): Promise<string> => {
  const response = await axios.post<{ reply: string }>(`${API_BASE}/chat`, {
    message,
    triage_context: triageContext,
  });
  return response.data.reply;
};

export const fetchResearchMetrics = async (): Promise<ResearchMetricsResponse> => {
  const response = await axios.get<ResearchMetricsResponse>(`${API_BASE}/research/metrics`);
  return response.data;
};
