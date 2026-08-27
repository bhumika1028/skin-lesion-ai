import React from 'react';
import { Activity, ShieldCheck, Cpu, GitMerge, FileText, ArrowRight, BarChart2 } from 'lucide-react';

interface HomePageProps {
  onStartTriage: () => void;
  onViewDashboard: () => void;
}

export const HomePage: React.FC<HomePageProps> = ({ onStartTriage, onViewDashboard }) => {
  return (
    <div className="space-y-12 py-6">
      {/* Hero Section */}
      <div className="relative rounded-3xl bg-gradient-to-br from-slate-900 via-slate-800 to-teal-950 text-white p-8 sm:p-12 overflow-hidden shadow-xl">
        <div className="absolute right-0 top-0 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="max-w-2xl relative z-10 space-y-6">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-teal-500/20 border border-teal-400/30 text-teal-300 text-xs font-semibold">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>AI Clinical Triage Research System</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
            AI-Assisted Skin Lesion Screening & <span className="text-teal-400">Uncertainty-Aware Risk Triage</span>
          </h1>

          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            Combining <strong>Swin Transformer</strong> visual feature extraction, <strong>clinical questionnaire metadata</strong> via cross-attention fusion, and <strong>Evidential Deep Learning (EDL)</strong> for Dirichlet-based uncertainty quantification.
          </p>

          <div className="flex flex-wrap gap-4 pt-2">
            <button
              onClick={onStartTriage}
              className="px-6 py-3.5 rounded-xl bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold text-sm shadow-lg shadow-teal-500/25 transition flex items-center space-x-2 cursor-pointer"
            >
              <Activity className="w-5 h-5" />
              <span>Analyze Lesion Image</span>
            </button>
            <button
              onClick={onViewDashboard}
              className="px-6 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-white font-medium text-sm transition flex items-center space-x-2 cursor-pointer"
            >
              <BarChart2 className="w-5 h-5" />
              <span>View Evaluation Benchmarks</span>
            </button>
          </div>
        </div>
      </div>

      {/* Feature Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center font-bold">
            <Cpu className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Swin Transformer Backbone</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Hierarchical shifted-window vision transformer extracting fine-grained textural irregularities and global morphological structures from 224×224 dermoscopic images.
          </p>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center font-bold">
            <GitMerge className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Multimodal Attention Fusion</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Cross-attention module allowing clinical questionnaire variables (Age, Sex, Location, Evolution, Symptoms, Allergies, Medications) to attend to spatial visual feature maps.
          </p>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center font-bold">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Evidential Uncertainty Engine</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Replaces standard Softmax overconfidence with Dirichlet distribution parameters to compute epistemic uncertainty ($u = K / S$) and route ambiguous cases to expert review.
          </p>
        </div>
      </div>

      {/* Trust Notice */}
      <div className="p-6 bg-slate-100 rounded-2xl border border-slate-200 text-xs text-slate-600 leading-relaxed flex items-start space-x-3">
        <FileText className="w-5 h-5 text-teal-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold text-slate-800 block mb-1">Clinical Screening Information</span>
          DermTriage AI provides clinical risk assessment and biopsy guidance. This system supports clinical decision-making and patient awareness. For biopsy execution or surgical procedures, consult a certified dermatologist.
        </div>
      </div>
    </div>
  );
};
