import React from 'react';
import { MapPin, User, Check } from 'lucide-react';

interface BodyMapSelectorProps {
  selectedLocation: string;
  onSelectLocation: (location: string) => void;
}

const LOCATION_OPTIONS = [
  { id: 'head/neck', label: 'Head / Neck / Face', icon: '👤', description: 'Sun-exposed scalp, forehead, cheeks, neck' },
  { id: 'anterior torso', label: 'Anterior Torso (Chest/Abdomen)', icon: '👕', description: 'Front chest, stomach, ribs' },
  { id: 'posterior torso', label: 'Posterior Torso (Back)', icon: '🎒', description: 'Upper/lower back, shoulders' },
  { id: 'upper extremity', label: 'Upper Extremity (Arm/Hand)', icon: '💪', description: 'Biceps, forearm, back of hand' },
  { id: 'lower extremity', label: 'Lower Extremity (Leg/Foot)', icon: '🦵', description: 'Thigh, shin, calf, top of foot' },
  { id: 'palms/soles', label: 'Palms / Soles (Acral)', icon: '✋', description: 'Palms of hands or soles of feet' },
  { id: 'oral/genital', label: 'Mucosal / Oral / Genital', icon: '👄', description: 'Mucosal skin surfaces' }
];

export const BodyMapSelector: React.FC<BodyMapSelectorProps> = ({ selectedLocation, onSelectLocation }) => {
  return (
    <div className="space-y-3">
      <label className="block font-semibold text-slate-700 text-xs flex items-center space-x-1">
        <MapPin className="w-3.5 h-3.5 text-teal-600" />
        <span>Anatomical Lesion Location (Interactive Body Map)</span>
      </label>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
        {LOCATION_OPTIONS.map((loc) => {
          const isSelected = selectedLocation.toLowerCase() === loc.id.toLowerCase();
          return (
            <button
              key={loc.id}
              type="button"
              onClick={() => onSelectLocation(loc.id)}
              className={`p-3 rounded-xl border text-left transition flex items-start justify-between cursor-pointer ${
                isSelected
                  ? 'border-teal-500 bg-teal-50/70 ring-2 ring-teal-500/20 text-slate-900 shadow-xs'
                  : 'border-slate-200 bg-slate-50/50 hover:bg-slate-100/70 text-slate-700'
              }`}
            >
              <div className="flex items-start space-x-2.5">
                <span className="text-base leading-none">{loc.icon}</span>
                <div>
                  <span className="font-bold block text-xs">{loc.label}</span>
                  <span className="text-[11px] text-slate-500 block leading-tight">{loc.description}</span>
                </div>
              </div>
              {isSelected && (
                <div className="w-4 h-4 rounded-full bg-teal-600 text-white flex items-center justify-center shrink-0">
                  <Check className="w-3 h-3" />
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};
