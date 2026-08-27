import React, { useState } from 'react';
import { ImageUploader } from '../components/ImageUploader';
import { ClinicalForm } from '../components/ClinicalForm';
import { ResultCard } from '../components/ResultCard';
import { submitTriageAnalysis } from '../services/api';
import { ClinicalFormData, ImageQualityResult, PredictionResponse } from '../types/triage';
import { Activity, Loader2 } from 'lucide-react';

export const TriagePage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [qualityResult, setQualityResult] = useState<ImageQualityResult | null>(null);

  const [formData, setFormData] = useState<ClinicalFormData>({
    age: 45,
    sex: 'Male',
    lesion_location: 'anterior torso',
    evolution: 'static',
    itching: false,
    bleeding: false,
    pain: false,
    observed_color: 'brown',
    prior_allergies: false,
    allergy_details: '',
    ongoing_medications: false,
    medication_details: '',
    model_architecture: 'swin_edl',
    imaging_mode: 'dermoscopic',
    fitzpatrick_scale: 'Type III (Medium / Olive)',
  });

  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [result, setResult] = useState<PredictionResponse | null>(null);

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert('Please upload a skin lesion image before analyzing.');
      return;
    }

    setIsLoading(true);
    setLoadingStep('Screening image quality & resolution...');

    try {
      if (formData.model_architecture === 'monte_carlo') {
        setTimeout(() => setLoadingStep('Executing T=10 Bayesian Monte Carlo stochastic passes...'), 600);
        setTimeout(() => setLoadingStep('Calculating Bayesian predictive variance across passes...'), 1200);
      } else if (formData.model_architecture === 'mobile_vit') {
        setTimeout(() => setLoadingStep('Extracting MobileViT edge features...'), 600);
        setTimeout(() => setLoadingStep('Fusing clinical metadata...'), 1200);
      } else {
        setTimeout(() => setLoadingStep('Extracting Swin Transformer visual features...'), 600);
        setTimeout(() => setLoadingStep('Fusing clinical metadata & patient history via cross-attention...'), 1200);
        setTimeout(() => setLoadingStep('Estimating Dirichlet epistemic uncertainty & risk level...'), 1800);
      }

      const data = await submitTriageAnalysis(selectedFile, formData);
      setResult(data);
    } catch (err: any) {
      console.error('Triage analysis error:', err);
      alert(err?.response?.data?.detail || 'An error occurred during triage analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setQualityResult(null);
    setResult(null);
  };

  if (result) {
    return <ResultCard result={result} onReset={handleReset} />;
  }

  return (
    <div className="space-y-6 py-4 max-w-4xl mx-auto">
      <div className="text-center space-y-1">
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Skin Lesion Clinical Triage Wizard</h2>
        <p className="text-xs text-slate-500">Select model engine, image mode, upload lesion photo, and complete patient history.</p>
      </div>

      <ImageUploader
        selectedFile={selectedFile}
        setSelectedFile={setSelectedFile}
        previewUrl={previewUrl}
        setPreviewUrl={setPreviewUrl}
        qualityResult={qualityResult}
        setQualityResult={setQualityResult}
      />

      <ClinicalForm formData={formData} setFormData={setFormData} />

      {/* Analyze Button / Loading State */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 text-center shadow-sm">
        {isLoading ? (
          <div className="py-6 space-y-3">
            <Loader2 className="w-8 h-8 animate-spin text-teal-600 mx-auto" />
            <p className="text-sm font-semibold text-slate-800">{loadingStep}</p>
            <p className="text-xs text-slate-400">Processing selected inference architecture...</p>
          </div>
        ) : (
          <button
            onClick={handleAnalyze}
            disabled={!selectedFile}
            className={`w-full py-4 rounded-xl font-bold text-sm shadow-md transition flex items-center justify-center space-x-2 ${
              selectedFile
                ? 'bg-teal-600 hover:bg-teal-700 text-white shadow-teal-600/20 cursor-pointer'
                : 'bg-slate-200 text-slate-400 cursor-not-allowed'
            }`}
          >
            <Activity className="w-5 h-5" />
            <span>Analyze Skin Lesion & Compute Uncertainty</span>
          </button>
        )}
      </div>
    </div>
  );
};
