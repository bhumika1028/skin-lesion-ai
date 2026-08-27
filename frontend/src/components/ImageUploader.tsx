import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, CheckCircle, AlertTriangle, RefreshCw } from 'lucide-react';
import { checkImageQuality } from '../services/api';
import { ImageQualityResult } from '../types/triage';

interface ImageUploaderProps {
  selectedFile: File | null;
  setSelectedFile: (file: File | null) => void;
  previewUrl: string | null;
  setPreviewUrl: (url: string | null) => void;
  qualityResult: ImageQualityResult | null;
  setQualityResult: (res: ImageQualityResult | null) => void;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({
  selectedFile,
  setSelectedFile,
  previewUrl,
  setPreviewUrl,
  qualityResult,
  setQualityResult,
}) => {
  const [isChecking, setIsChecking] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (file: File) => {
    if (!file.type.startsWith('image/')) {
      alert('Please upload a valid image file (JPG, JPEG, PNG).');
      return;
    }

    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);

    // Pre-check quality
    setIsChecking(true);
    try {
      const res = await checkImageQuality(file);
      setQualityResult(res);
    } catch (err) {
      console.warn('Quality pre-check fallback:', err);
    } finally {
      setIsChecking(false);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleLoadSampleImage = (sampleType: 'melanoma' | 'nevus' | 'keratosis') => {
    const canvas = document.createElement('canvas');
    canvas.width = 224;
    canvas.height = 224;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.fillStyle = sampleType === 'melanoma' ? '#d4a373' : (sampleType === 'nevus' ? '#e9edc9' : '#faedcd');
      ctx.fillRect(0, 0, 224, 224);

      ctx.beginPath();
      if (sampleType === 'melanoma') {
        ctx.ellipse(112, 112, 60, 42, Math.PI / 4, 0, 2 * Math.PI);
        ctx.fillStyle = '#2b1e16';
      } else if (sampleType === 'nevus') {
        ctx.arc(112, 112, 45, 0, 2 * Math.PI);
        ctx.fillStyle = '#6b4226';
      } else {
        ctx.arc(112, 112, 38, 0, 2 * Math.PI);
        ctx.fillStyle = '#8b5a2b';
      }
      ctx.fill();

      canvas.toBlob((blob) => {
        if (blob) {
          const file = new File([blob], `sample_${sampleType}.jpg`, { type: 'image/jpeg' });
          handleFileChange(file);
        }
      }, 'image/jpeg');
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <h3 className="text-base font-semibold text-slate-900 mb-1 flex items-center space-x-2">
        <UploadCloud className="w-5 h-5 text-teal-600" />
        <span>Step 1: Upload Dermoscopic Skin Image</span>
      </h3>
      <p className="text-xs text-slate-500 mb-4">
        Upload a clear, well-lit image of the skin lesion (JPG or PNG formats supported).
      </p>

      {!previewUrl ? (
        <div className="space-y-3">
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:border-teal-500 hover:bg-teal-50/50 transition cursor-pointer group"
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={(e) => e.target.files?.[0] && handleFileChange(e.target.files[0])}
              accept="image/png, image/jpeg, image/jpg"
              className="hidden"
            />
            <div className="w-14 h-14 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-3 text-slate-400 group-hover:bg-teal-100 group-hover:text-teal-600 transition">
              <ImageIcon className="w-7 h-7" />
            </div>
            <p className="text-sm font-medium text-slate-700">
              Drag and drop lesion image here, or <span className="text-teal-600 font-semibold underline">browse</span>
            </p>
            <p className="text-xs text-slate-400 mt-1">Recommended size: 224×224 px or higher</p>
          </div>

          {/* Quick Demo Sample Image Presets */}
          <div className="flex flex-wrap items-center justify-between gap-2 p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
            <span className="font-semibold text-slate-700 flex items-center space-x-1">
              <span>🧪 Quick Demo Presets:</span>
            </span>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={() => handleLoadSampleImage('melanoma')}
                className="px-3 py-1.5 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 font-medium transition cursor-pointer"
              >
                Sample Melanoma (Suspicious)
              </button>
              <button
                type="button"
                onClick={() => handleLoadSampleImage('nevus')}
                className="px-3 py-1.5 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-800 border border-indigo-200 font-medium transition cursor-pointer"
              >
                Sample Nevus (Benign)
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="relative rounded-xl overflow-hidden border border-slate-200 bg-slate-900 flex justify-center items-center max-h-72">
            <img src={previewUrl} alt="Skin Lesion Preview" className="max-h-72 object-contain" />
            <button
              onClick={() => {
                setSelectedFile(null);
                setPreviewUrl(null);
                setQualityResult(null);
              }}
              className="absolute top-3 right-3 bg-slate-900/80 hover:bg-slate-900 text-white text-xs px-3 py-1.5 rounded-lg backdrop-blur-sm transition flex items-center space-x-1"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Change Image</span>
            </button>
          </div>

          {/* Quality Screening Feedback */}
          {isChecking ? (
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center space-x-2 text-xs text-slate-600">
              <RefreshCw className="w-4 h-4 animate-spin text-teal-600" />
              <span>Running automated image quality assessment...</span>
            </div>
          ) : qualityResult && (
            <div
              className={`p-4 rounded-xl border text-xs leading-relaxed ${
                qualityResult.is_valid
                  ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
                  : 'bg-amber-50 border-amber-200 text-amber-900'
              }`}
            >
              <div className="flex items-center space-x-2 font-semibold mb-1">
                {qualityResult.is_valid ? (
                  <CheckCircle className="w-4 h-4 text-emerald-600" />
                ) : (
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                )}
                <span>
                  Image Quality: {qualityResult.is_valid ? 'Pass (Good Quality)' : 'Quality Warning'}
                </span>
              </div>
              <p className="mt-0.5">{qualityResult.message}</p>
              <div className="mt-2 grid grid-cols-3 gap-2 text-[11px] font-mono text-slate-600 bg-white/60 p-2 rounded-lg border border-slate-200/60">
                <div>Res: {qualityResult.resolution}</div>
                <div>Blur Var: {qualityResult.blur_variance}</div>
                <div>Score: {Math.round(qualityResult.overall_score * 100)}%</div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
