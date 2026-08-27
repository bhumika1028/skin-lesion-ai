import React from 'react';
import { Activity, ShieldCheck, BarChart3, BookOpen, HeartPulse, TrendingUp } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
          <div 
            onClick={() => setActiveTab('home')}
            className="flex items-center space-x-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-teal-600 flex items-center justify-center text-white shadow-md shadow-teal-600/20 group-hover:bg-teal-700 transition">
              <HeartPulse className="w-6 h-6" />
            </div>
            <div>
              <span className="text-lg font-bold text-slate-900 tracking-tight">DermTriage <span className="text-teal-600">AI</span></span>
              <span className="block text-xs text-slate-500 font-medium">Uncertainty-Aware Clinical Screening</span>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex space-x-1">
            <button
              onClick={() => setActiveTab('home')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === 'home' 
                  ? 'bg-teal-50 text-teal-700 font-semibold' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              Home
            </button>
            <button
              onClick={() => setActiveTab('triage')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition flex items-center space-x-1.5 ${
                activeTab === 'triage' 
                  ? 'bg-teal-600 text-white shadow-sm shadow-teal-600/20' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <Activity className="w-4 h-4" />
              <span>Analyze Lesion</span>
            </button>
            <button
              onClick={() => setActiveTab('tracker')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition flex items-center space-x-1.5 ${
                activeTab === 'tracker' 
                  ? 'bg-teal-50 text-teal-700 font-semibold' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <TrendingUp className="w-4 h-4" />
              <span>Evolution Tracker</span>
            </button>
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition flex items-center space-x-1.5 ${
                activeTab === 'dashboard' 
                  ? 'bg-teal-50 text-teal-700 font-semibold' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              <span>Evaluation Benchmarks</span>
            </button>
            <button
              onClick={() => setActiveTab('learn')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition flex items-center space-x-1.5 ${
                activeTab === 'learn' 
                  ? 'bg-teal-50 text-teal-700 font-semibold' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Clinical Architecture</span>
            </button>
          </nav>

          {/* Safety Badge */}
          <div className="flex items-center space-x-2 text-xs text-teal-800 bg-teal-50 px-3.5 py-1.5 rounded-full border border-teal-200 font-medium">
            <ShieldCheck className="w-4 h-4 text-teal-600" />
            <span className="hidden sm:inline">AI Clinical Triage Research System</span>
          </div>
        </div>
      </div>
    </header>
  );
};
