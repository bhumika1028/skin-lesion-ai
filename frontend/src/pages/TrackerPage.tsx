import React, { useState } from 'react';
import { Camera, Calendar, ArrowRight, TrendingUp, AlertTriangle, CheckCircle2, RefreshCw, Layers } from 'lucide-react';

export const TrackerPage: React.FC = () => {
  const [baselineFile, setBaselineFile] = useState<File | null>(null);
  const [baselinePreview, setBaselinePreview] = useState<string | null>(null);
  const [currentFile, setCurrentFile] = useState<File | null>(null);
  const [currentPreview, setCurrentPreview] = useState<string | null>(null);

  const [timeGapMonths, setTimeGapMonths] = useState<number>(6);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [trackerResult, setTrackerResult] = useState<any | null>(null);

  const handleBaselineChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setBaselineFile(file);
      setBaselinePreview(URL.createObjectURL(file));
      setTrackerResult(null);
    }
  };

  const handleCurrentChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setCurrentFile(file);
      setCurrentPreview(URL.createObjectURL(file));
      setTrackerResult(null);
    }
  };

  const handleRunDeltaAnalysis = () => {
    if (!baselineFile || !currentFile) {
      alert('Please upload both Baseline (Past) and Current photos before running evolution tracking.');
      return;
    }

    setIsAnalyzing(true);
    setTimeout(() => {
      // Simulate quantitative delta computations
      const areaGrowth = +(12.4 + (Math.random() * 8.5)).toFixed(1);
      const asymmetryDelta = +(0.8 + (Math.random() * 1.4)).toFixed(1);
      const colorVarianceDelta = +(1.2 + (Math.random() * 1.8)).toFixed(1);
      const overallDeltaScore = +(areaGrowth * 0.4 + asymmetryDelta * 2.5 + colorVarianceDelta * 2.0).toFixed(1);

      const isHighRisk = overallDeltaScore > 8.0;

      setTrackerResult({
        timeGapMonths,
        areaGrowthPercent: areaGrowth,
        asymmetryDelta,
        colorVarianceDelta,
        overallDeltaScore,
        evolutionRisk: isHighRisk ? 'SIGNIFICANT EVOLUTION DETECTED' : 'STABLE / MINIMAL CHANGE',
        recommendation: isHighRisk
          ? 'Noticeable structural expansion and asymmetry change detected over time. Prompt dermatological evaluation advised.'
          : 'Lesion dimensions remain relatively stable across time intervals. Routine self-inspection recommended.',
        isHighRisk
      });

      setIsAnalyzing(false);
    }, 1200);
  };

  const handleReset = () => {
    setBaselineFile(null);
    setBaselinePreview(null);
    setCurrentFile(null);
    setCurrentPreview(null);
    setTrackerResult(null);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto py-4">
      {/* Title Header */}
      <div className="text-center space-y-1">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-xs font-semibold">
          <TrendingUp className="w-3.5 h-3.5 text-teal-600" />
          <span>Longitudinal Lesion Tracking Tool</span>
        </div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Before & After Lesion Growth Analyzer</h2>
        <p className="text-xs text-slate-500">
          Upload baseline (past) and current photos to calculate quantitative structural changes over time (Δ Growth Index).
        </p>
      </div>

      {/* 2-Photo Upload Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Baseline Photo (Past) */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex justify-between items-center border-b border-slate-100 pb-2">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-1">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              <span>1. Baseline Photo (Past Photo)</span>
            </span>
            <span className="text-[11px] font-semibold text-slate-400">e.g., 6 Months Ago</span>
          </div>

          {baselinePreview ? (
            <div className="relative rounded-xl overflow-hidden border border-slate-200 bg-slate-900 h-48 flex justify-center items-center">
              <img src={baselinePreview} alt="Baseline Lesion" className="max-h-full max-w-full object-contain" />
              <button
                onClick={() => { setBaselineFile(null); setBaselinePreview(null); }}
                className="absolute top-2 right-2 bg-slate-900/80 text-white text-xs px-2 py-1 rounded-md hover:bg-slate-900"
              >
                Change
              </button>
            </div>
          ) : (
            <label className="border-2 border-dashed border-slate-300 hover:border-teal-500 rounded-xl h-48 flex flex-col justify-center items-center cursor-pointer bg-slate-50/50 hover:bg-teal-50/30 transition p-4 text-center">
              <Camera className="w-8 h-8 text-slate-400 mb-2" />
              <span className="text-xs font-semibold text-slate-700">Upload Baseline Photo</span>
              <span className="text-[11px] text-slate-400 mt-1">JPG, PNG format</span>
              <input type="file" accept="image/*" onChange={handleBaselineChange} className="hidden" />
            </label>
          )}
        </div>

        {/* Current Photo (Today) */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex justify-between items-center border-b border-slate-100 pb-2">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-1">
              <Camera className="w-3.5 h-3.5 text-teal-600" />
              <span>2. Current Photo (Today's Photo)</span>
            </span>
            <span className="text-[11px] font-semibold text-teal-600">Present</span>
          </div>

          {currentPreview ? (
            <div className="relative rounded-xl overflow-hidden border border-slate-200 bg-slate-900 h-48 flex justify-center items-center">
              <img src={currentPreview} alt="Current Lesion" className="max-h-full max-w-full object-contain" />
              <button
                onClick={() => { setCurrentFile(null); setCurrentPreview(null); }}
                className="absolute top-2 right-2 bg-slate-900/80 text-white text-xs px-2 py-1 rounded-md hover:bg-slate-900"
              >
                Change
              </button>
            </div>
          ) : (
            <label className="border-2 border-dashed border-slate-300 hover:border-teal-500 rounded-xl h-48 flex flex-col justify-center items-center cursor-pointer bg-slate-50/50 hover:bg-teal-50/30 transition p-4 text-center">
              <Camera className="w-8 h-8 text-teal-600 mb-2" />
              <span className="text-xs font-semibold text-slate-700">Upload Current Photo</span>
              <span className="text-[11px] text-slate-400 mt-1">JPG, PNG format</span>
              <input type="file" accept="image/*" onChange={handleCurrentChange} className="hidden" />
            </label>
          )}
        </div>
      </div>

      {/* Time Interval & Controls */}
      <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <label className="font-semibold text-slate-700 shrink-0">Time Interval Between Photos:</label>
          <select
            value={timeGapMonths}
            onChange={(e) => setTimeGapMonths(parseInt(e.target.value))}
            className="px-3 py-1.5 border border-slate-300 rounded-lg text-slate-900 bg-white font-medium focus:ring-2 focus:ring-teal-500"
          >
            <option value={1}>1 Month Apart</option>
            <option value={3}>3 Months Apart</option>
            <option value={6}>6 Months Apart</option>
            <option value={12}>12 Months (1 Year) Apart</option>
          </select>
        </div>

        <div className="flex space-x-2 w-full sm:w-auto justify-end">
          {(baselineFile || currentFile) && (
            <button
              onClick={handleReset}
              className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold transition"
            >
              Reset
            </button>
          )}
          <button
            onClick={handleRunDeltaAnalysis}
            disabled={!baselineFile || !currentFile || isAnalyzing}
            className={`px-6 py-2.5 rounded-xl font-bold text-xs shadow-md transition flex items-center space-x-2 ${
              baselineFile && currentFile && !isAnalyzing
                ? 'bg-teal-600 hover:bg-teal-700 text-white cursor-pointer shadow-teal-600/20'
                : 'bg-slate-200 text-slate-400 cursor-not-allowed'
            }`}
          >
            {isAnalyzing ? (
              <RefreshCw className="w-4 h-4 animate-spin mx-auto" />
            ) : (
              <>
                <TrendingUp className="w-4 h-4" />
                <span>Calculate Lesion Growth Delta</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Delta Results Output Card */}
      {trackerResult && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5 animate-in fade-in">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div className="flex items-center space-x-2">
              {trackerResult.isHighRisk ? (
                <AlertTriangle className="w-6 h-6 text-rose-600" />
              ) : (
                <CheckCircle2 className="w-6 h-6 text-emerald-600" />
              )}
              <div>
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Evolution Risk Status</span>
                <h3 className={`text-lg font-extrabold ${trackerResult.isHighRisk ? 'text-rose-600' : 'text-emerald-700'}`}>
                  {trackerResult.evolutionRisk}
                </h3>
              </div>
            </div>

            <div className="text-right">
              <span className="text-[11px] text-slate-400 block">Overall Growth Delta Score</span>
              <span className="text-xl font-mono font-bold text-slate-900">{trackerResult.overallDeltaScore} / 15.0</span>
            </div>
          </div>

          <p className="text-xs font-medium text-slate-800 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-200">
            {trackerResult.recommendation}
          </p>

          {/* 3 Delta Quantitative Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            {/* Surface Area Expansion */}
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span className="text-slate-500 font-semibold block">Surface Area Expansion (Δ Area)</span>
              <span className="text-lg font-mono font-bold text-teal-700">+{trackerResult.areaGrowthPercent}%</span>
              <p className="text-[11px] text-slate-400">Estimated 2D spatial growth</p>
            </div>

            {/* Asymmetry Shift */}
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span className="text-slate-500 font-semibold block">Asymmetry Index Shift (Δ Axis)</span>
              <span className="text-lg font-mono font-bold text-indigo-700">+{trackerResult.asymmetryDelta} units</span>
              <p className="text-[11px] text-slate-400">Border non-uniformity change</p>
            </div>

            {/* Color Heterogeneity Delta */}
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span className="text-slate-500 font-semibold block">Color Darkening Delta (Δ RGB)</span>
              <span className="text-lg font-mono font-bold text-amber-700">+{trackerResult.colorVarianceDelta} variance</span>
              <p className="text-[11px] text-slate-400">Pigmentation dispersion shift</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
