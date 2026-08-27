import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { HomePage } from './pages/HomePage';
import { TriagePage } from './pages/TriagePage';
import { TrackerPage } from './pages/TrackerPage';
import { DashboardPage } from './pages/DashboardPage';
import { LearnPage } from './pages/LearnPage';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('home');

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between">
      <div>
        <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {activeTab === 'home' && (
            <HomePage
              onStartTriage={() => setActiveTab('triage')}
              onViewDashboard={() => setActiveTab('dashboard')}
            />
          )}
          {activeTab === 'triage' && <TriagePage />}
          {activeTab === 'tracker' && <TrackerPage />}
          {activeTab === 'dashboard' && <DashboardPage />}
          {activeTab === 'learn' && <LearnPage />}
        </main>
      </div>

      <footer className="bg-white border-t border-slate-200 py-6 mt-12 text-xs text-slate-500 text-center">
        <div className="max-w-7xl mx-auto px-4">
          <p className="font-semibold text-slate-700">DermTriage AI - Advanced Clinical Screening Platform</p>
          <p className="mt-1">Multimodal Swin Transformer & Dirichlet Evidential Uncertainty Quantification</p>
        </div>
      </footer>
    </div>
  );
};
