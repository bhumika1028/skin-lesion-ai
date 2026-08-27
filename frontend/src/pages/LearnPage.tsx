import React from 'react';
import { BookOpen, ShieldCheck, GitBranch, Layers, FileText } from 'lucide-react';

export const LearnPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto py-6 space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center space-x-2">
          <BookOpen className="w-6 h-6 text-teal-600" />
          <span>Research Methodology & System Architecture</span>
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          Technical specifications for Swin Transformer, Multimodal Attention, and Dirichlet Evidential Deep Learning.
        </p>
      </div>

      <div className="space-y-6 text-sm text-slate-700 leading-relaxed">
        {/* Section 1 */}
        <section className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <Layers className="w-5 h-5 text-teal-600" />
            <span>1. Swin Transformer Visual Encoder</span>
          </h3>
          <p>
            Unlike standard Vision Transformers (ViT) with fixed patch resolutions, the <strong>Swin Transformer</strong> extracts visual features hierarchically across 4 stages. Using Shifted Window self-attention (W-MSA & SW-MSA), it captures both subtle local pigment networks and large-scale structural asymmetry without quadratic computational scaling.
          </p>
        </section>

        {/* Section 2 */}
        <section className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <GitBranch className="w-5 h-5 text-teal-600" />
            <span>2. Cross-Attention Multimodal Fusion</span>
          </h3>
          <p>
            Traditional multimodal models simply concatenate tabular metadata with image vectors. In contrast, our cross-attention mechanism treats clinical metadata (Age, Sex, Location, Evolution, Symptoms) as the <strong>Query ($Q$)</strong>, allowing non-visual context to dynamically re-weight visual feature maps (Keys $K$ and Values $V$).
          </p>
        </section>

        {/* Section 3 */}
        <section className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <ShieldCheck className="w-5 h-5 text-teal-600" />
            <span>3. Dirichlet Evidential Deep Learning (EDL)</span>
          </h3>
          <p>
            Standard neural network Softmax layers produce overconfident predictions. EDL models evidence output $e_k \ge 0$ parameterizing a <strong>Dirichlet distribution</strong> ($\alpha_k = e_k + 1$). Total Dirichlet strength $S = \sum \alpha_k$ directly yields epistemic uncertainty $u = K / S$, enabling safe referral of ambiguous or out-of-distribution cases to expert review.
          </p>
        </section>
      </div>
    </div>
  );
};
